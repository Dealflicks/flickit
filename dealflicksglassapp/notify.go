// Copyright (C) 2013 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package quickstart

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"

	"code.google.com/p/goauth2/oauth"
	"code.google.com/p/google-api-go-client/mirror/v1"

	"appengine"
	"appengine/taskqueue"
	"appengine/urlfetch"
	"appengine/blobstore"
)

// Because App Engine owns main and starts the HTTP service,
// we do our setup during initialization.
func init() {
	http.HandleFunc("/notify", errorAdapter(notifyHandler))
	http.HandleFunc("/processnotification", notifyProcessorHandler)
}

// notifyHandler starts a new Task Queue to process the notification ping.
func notifyHandler(w http.ResponseWriter, r *http.Request) error {
	c := appengine.NewContext(r)
	t := &taskqueue.Task{
		Path:   "/processnotification",
		Method: "POST",
		Header: r.Header,
	}
	payload, err := ioutil.ReadAll(r.Body)
	if err != nil {
		return fmt.Errorf("Unable to read request body: %s", err)
	}
	t.Payload = payload
	// Insert a new Task in the default Task Queue.
	if _, err = taskqueue.Add(c, t, ""); err != nil {
		return fmt.Errorf("Failed to add new task: %s", err)
	}
	return nil
}

// notifyProcessorHandler processes notification pings from the API in a Task Queue.
func notifyProcessorHandler(w http.ResponseWriter, r *http.Request) {
	c := appengine.NewContext(r)

	not := new(mirror.Notification)
	if err := json.NewDecoder(r.Body).Decode(not); err != nil {
		c.Errorf("Unable to decode notification: %v", err)
		return
	}
	userId := not.UserToken
	t := authTransport(c, userId)
	if t == nil {
		c.Errorf("Unknown user ID: %s", userId)
		return
	}
	svc, _ := mirror.New(t.Client())

	var err error
	if not.Collection == "locations" {
		err = handleLocationsNotification(c, svc, not)
	} else if not.Collection == "timeline" {
		err = handleTimelineNotification(c, svc, not, t)
	}
	if err != nil {
		c.Errorf("Error occured while processing notification: %s", err)
	}
}

// handleLocationsNotification processes a location notification.
func handleLocationsNotification(c appengine.Context, svc *mirror.Service, not *mirror.Notification) error {
	l, err := svc.Locations.Get(not.ItemId).Do()
	if err != nil {
		return fmt.Errorf("Unable to retrieve location: %s", err)
	}
	text := fmt.Sprintf("Go Quick Start says you are at %f by %f.", l.Latitude, l.Longitude)
	t := &mirror.TimelineItem{
		Text:         text,
		Location:     l,
		MenuItems:    []*mirror.MenuItem{&mirror.MenuItem{Action: "NAVIGATE"}},
		Notification: &mirror.NotificationConfig{Level: "DEFAULT"},
	}
	_, err = svc.Timeline.Insert(t).Do()
	if err != nil {
		return fmt.Errorf("Unable to insert timeline item: %s", err)
	}
	return nil
}

// handleTimelineNotification processes a timeline notification.
func handleTimelineNotification(c appengine.Context, svc *mirror.Service, not *mirror.Notification, transport *oauth.Transport) error {
	for _, ua := range not.UserActions {
		if ua.Type != "SHARE" {
			c.Infof("I don't know what to do with this notification: %+v", ua)
			continue
		}
		t, err := svc.Timeline.Get(not.ItemId).Do()
		if err != nil {
			return fmt.Errorf("Unable to retrieve timeline item: %s", err)
		}
		// We could have just updated the Text attribute in-place and used the
		// Update method instead, but we wanted to illustrate the Patch method
		// here.
		patch := &mirror.TimelineItem{
			Text: fmt.Sprintf("You flicked your photo! %s", t.Text),
		}
		_, err = svc.Timeline.Patch(not.ItemId, patch).Do()
		if err != nil {
			return fmt.Errorf("Unable to patch timeline item: %s", err)
		}

		// Here is the place where we handle the notification
		c.Infof("##### PHOTO PUBLIC URL: %v", t.Attachments)
		for _, attachment := range t.Attachments {
			c.Infof("attachment %v", attachment.ContentUrl)
			c.Infof("is processing? %v", attachment.IsProcessingContent)
			// url := fmt.Sprintf("/attachmentproxy?attachment=%s&timelineItem=%s", attachment.Id, t.Id)
			// c.Infof("Image URL %v", url)


			itemId := t.Id
			attachmentId := attachment.Id

			// userId, err := userID(c)
			// if err != nil {
			// 	return err
			// }
			// t := authTransport(c, userId)
			svc, err := mirror.New(transport.Client())
			if err != nil {
				return err
			}
			if itemId == "" || attachmentId == "" {
				// http.Error(w, "", http.StatusBadRequest)
				return nil
			}
			a, err := svc.Timeline.Attachments.Get(itemId, attachmentId).Do()
			if err != nil {
				return err
			}
			req, err := http.NewRequest("GET", a.ContentUrl, nil)
			if err != nil {
				return err
			}

			resp, err := transport.RoundTrip(req)
			if err != nil {
				return err
			}
			defer resp.Body.Close()
			// w.Header().Set("Content-Type", resp.Header.Get("Content-Type"))
			bytes, _ := ioutil.ReadAll(resp.Body)

			wrt, err := blobstore.Create(c, "application/png")
			if err != nil {
			    // return k, 
			    c.Infof("ERR")
			    return nil
			}
			// _, _ := wrt.Write(bytes)
			wrt.Write(bytes)
			// if err != nil {
			//     c.Infof("ERR")
			//     return nil
			// }
			// c.Infof("#### %v", x)
			err = wrt.Close()
			// if err != nil {
			//     c.Infof("ERR")
			//     return nil
			// }
			k, _ := wrt.Key()
			c.Infof("####### %v", k)
			imageUrl := fmt.Sprintf("https://dealflicksglassapp.appspot.com/serve/?blobKey=%s", k)

			// resp, err = http.Get("http://10.10.2.208:9999")
			// defer resp.Body.Close()
			// bbb, _ := ioutil.ReadAll(resp.Body)
			// c.Infof(string(bbb))

			// resp, err = http.PostForm("http://10.10.2.208:9999/picture-string-search", url.Values{"imgstr": {string(bytes)}})
			// if err != nil {
			// 	// handle error
			// 	c.Infof("!!!! ERROR -- %s", err)
			// } else {
			// 	defer resp.Body.Close()
			// 	bbb, _ := ioutil.ReadAll(resp.Body)
			// 	c.Infof("****** %v", string(bbb))
			// }

			client := urlfetch.Client(c)

		    resp, err = client.PostForm("http://www.justflickit.com/picture-search", url.Values{"imgurl": {imageUrl}, "api_token": {"12345"}})
		    if err != nil {
		        // http.Error(w, err.Error(), http.StatusInternalServerError)
		    	c.Infof("**** %v", err)    
		        return nil
		    }
		    // fmt.Fprintf(w, "HTTP POST returned status %v", resp.Status)
		    bbb, _ := ioutil.ReadAll(resp.Body)
		    c.Infof("***** %v", string(bbb))

		    newPatch := &mirror.TimelineItem{
		    	Text: string(bbb),
		    }
		    _, err = svc.Timeline.Patch(not.ItemId, newPatch).Do()
		    if err != nil {
		    	return fmt.Errorf("Unable to patch timeline item: %s", err)
		    }

			//-------------
			// client := urlfetch.Client(c)
			// if resp, err := client.Get(url); err != nil {
			// 	c.Errorf("Unable to retrieve media: %s", err)
			// } else {
			// 	defer resp.Body.Close()
			// 	bytes, _ := ioutil.ReadAll(resp.Body)
			// 	c.Infof(string(bytes))

			// 	// req, _ := http.NewRequest("PUT", "https://myBucket.s3.amazonaws.com", nil)

			// 	// req.Header = map[string][]string {
			// 	// 	"X-amz-acl": {"public-read"},
			// 	// 	"Authorization": {"AWS AKIAJBYSRHEHDISAU55Q:cT+RrO3O4TJCJxG3Ssv0KJ+Ra5Hssi8csqDLm7cd"},
			// 	// 	"Host": {"flickit-static.s3.amazonaws.com"},
			// 	// 	"Content-Type": {"image/png"},
			// 	// }

			// 	// req.Body = resp.Body

			// 	// resp2, _ := client.Do(req)
			// 	// c.Infof("##### %v", resp2)
			// }

			// req, _ := http.NewRequest("PUT", "https://myBucket.s3.amazonaws.com", nil)

			// req.Header = map[string][]string {
			// 	"X-amz-acl": {"public-read"},
			// 	"Authorization": {"AWS AKIAJBYSRHEHDISAU55Q:cT+RrO3O4TJCJxG3Ssv0KJ+Ra5Hssi8csqDLm7cd"},
			// 	"Host": {"flickit-static.s3.amazonaws.com"},
			// 	"Content-Type": {"image/png"},
			// }

			// req.Body = resp.Body

			// resp2, _ := client.Do(req)
			// c.Infof("##### %v", resp2)

			// A header maps request lines to their values.
			       // If the header says
			       //
			       //	accept-encoding: gzip, deflate
			       //	Accept-Language: en-us
			       //	Connection: keep-alive
			       //
			       // then
			       //
			       //	Header = map[string][]string{
			       //		"Accept-Encoding": {"gzip, deflate"},
			       //		"Accept-Language": {"en-us"},
			       //		"Connection": {"keep-alive"},
			       //	}

			// AKIAJBYSRHEHDISAU55Q
			// cT+RrO3O4TJCJxG3Ssv0KJ+Ra5Hssi8csqDLm7cd

			// PUT TestObject.txt HTTP/1.1
			// Host: myBucket.s3.amazonaws.com
			// x-amz-date: Fri, 13 Apr 2012 05:54:57 GMT
			// x-amz-acl: public-read
			// Authorization: AWS AKIAIOSFODNN7EXAMPLE:xQE0diMbLRepdf3YB+FIEXAMPLE=
			// Content-Length: 300
			// Expect: 100-continue
			// Connection: Keep-Alive

		}

		// _, err = svc.Timeline.Patch(not.ItemId, patch).Do()
		// if err != nil {
		// 	return fmt.Errorf("Unable to patch timeline item: %s", err)
		// }
	}
	return nil
}
