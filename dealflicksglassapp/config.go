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

const (
	debug       = true // Set to false to turn off logging every API request.
	sessionName = "dealflicksglassapp"
	secret      = "very_secret" // Make it a random string

	// Created at http://code.google.com/apis/console, these identify
	// our app for the OAuth protocol.
	clientId     = "845479005981.apps.googleusercontent.com"
	clientSecret = "OyipLPm6Mhtn8By-b32z9MHD"
	scopes       = "https://www.googleapis.com/auth/glass.timeline " +
		"https://www.googleapis.com/auth/glass.location " +
		"https://www.googleapis.com/auth/userinfo.profile"
)
