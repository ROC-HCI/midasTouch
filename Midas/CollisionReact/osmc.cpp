/*
Copyright (c) 2009 Chris B Stones (welcometochrisworld.com)

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
*/

#include "osmc.h"
#include "Arduino.h"

//OSMC::osmc(int aHI,int bHI,int aLI,int bLI, int dis) {
//	this->aHI = aHI;
//	this->bHI = bHI;
//	this->aLI = aLI;
//	this->aLI = bLI;
//	this->dis = dis;
//}

void OSMC::init(int aHI,int bHI,int aLI,int bLI, int dis) {
this->aHI = aHI;
this->bHI = bHI;
this->aLI = aLI;
this->aLI = bLI;
this->dis = dis;
}

//OSMC::~OSMC() { /* nothing */}

void OSMC::forward(int s) {
  digitalWrite(     this->aHI, HIGH);
  digitalWrite(     this->bHI, HIGH);
  digitalWrite(     this->aLI, LOW);
   analogWrite(     this->bLI, s); 
  digitalWrite( this->dis, LOW);
}

void OSMC::reverse(int s) {
  digitalWrite(     this->aHI, HIGH);
  digitalWrite(     this->bHI, HIGH);
   analogWrite(     this->aLI, s); 
  digitalWrite(     this->bLI, LOW);
  digitalWrite( this->dis, LOW);
}

void OSMC::brake() {
  digitalWrite(     this->aHI, HIGH);
  digitalWrite(     this->bHI, HIGH);
  digitalWrite(     this->aLI, LOW);
  digitalWrite(     this->bLI, LOW);
  digitalWrite(     this->dis, LOW);
}

void OSMC::disable() {
digitalWrite( this->dis, HIGH);
}
