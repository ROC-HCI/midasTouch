// Leapmotiontest.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <string.h>
#include "leap.h"
using namespace Leap;
using namespace std;

class SampleListener : public Listener {
public:
	virtual void onInit(const Controller&);
	virtual void onConnect(const Controller&);
	virtual void onDisconnect(const Controller&);
	virtual void onExit(const Controller&);
	virtual void onFrame(const Controller&);
	virtual void onFocusGained(const Controller&);
	virtual void onFocusLost(const Controller&);
	virtual void onDeviceChange(const Controller&);
	virtual void onServiceConnect(const Controller&);
	virtual void onServiceDisconnect(const Controller&);

private:
};

const std::string fingerNames[] = { "Thumb", "Index", "Middle", "Ring", "Pinky" };
const std::string boneNames[] = { "Metacarpal", "Proximal", "Middle", "Distal" };
const std::string stateNames[] = { "STATE_INVALID", "STATE_START", "STATE_UPDATE", "STATE_END" };

void SampleListener::onInit(const Controller& controller) {
	std::cout << "Initialized" << std::endl;
}

void SampleListener::onConnect(const Controller& controller) {
	std::cout << "Connected" << std::endl;
	controller.enableGesture(Gesture::TYPE_CIRCLE);
	controller.enableGesture(Gesture::TYPE_KEY_TAP);
	controller.enableGesture(Gesture::TYPE_SCREEN_TAP);
	controller.enableGesture(Gesture::TYPE_SWIPE);
}

void SampleListener::onDisconnect(const Controller& controller) {
	// Note: not dispatched when running in a debugger.
	std::cout << "Disconnected" << std::endl;
}

void SampleListener::onExit(const Controller& controller) {
	std::cout << "Exited" << std::endl;
}

void SampleListener::onFrame(const Controller& controller) {
	// Get the most recent frame and report some basic information
	const Frame frame = controller.frame();
	
	//Initiate hand list
	HandList hands = frame.hands();

	//For each hand initiate fingers and pointables
	for (HandList::const_iterator hl = hands.begin(); hl != hands.end(); ++hl) {
		// Get the first hand
		const Hand hand = *hl;


		// Get the hand's normal vector and direction
		const Vector normal = hand.palmNormal();
		const Vector direction = hand.direction();


		

	
	/*  
		Frame Info
			Frame id: " << frame.id()
			timestamp: " << frame.timestamp()
			hands: " << frame.hands().count()
			fingers: " << frame.fingers().count()
			tools: " << frame.tools().count()
			gestures: " << frame.gestures().count()


		//Is the Hand a left hand or a right hand
			handType = hand.isLeft() ? "Left hand" : "Right hand";
		

		// Get the hand's normal vector and direction
			const Vector normal = hand.palmNormal();
			const Vector direction = hand.direction();


		// Calculate the hand's pitch, roll, and yaw angles
			normal.roll() * RAD_TO_DEG
			direction.yaw() * RAD_TO_DEG 


		// information on fingers calls
			finger.id()
			finger.length()
			finger.width()
			

		//Info on Bones
			bone.prevJoint()
			bone.nextJoint()
			bone.direction()
			
		*/

		



		// Get fingers
		const FingerList fingers = hand.fingers();
		//for (FingerList::const_iterator fl = fingers.begin(); fl != fingers.end(); ++fl) 
		{
			const Finger finger = fingers.frontmost();


			//std::cout << fingers.begin.tip_position.x;
			cout << finger.tipPosition() << "\n";
			
			
			// Get finger bones
			for (int b = 0; b < 4; ++b) {
				Bone::Type boneType = static_cast<Bone::Type>(b);
				Bone bone = finger.bone(boneType);

				
			}
		}
	}

	// Get tools
	const ToolList tools = frame.tools();
	for (ToolList::const_iterator tl = tools.begin(); tl != tools.end(); ++tl) {
		const Tool tool = *tl;
		std::cout << std::string(2, ' ') << "Tool, id: " << tool.id()
			<< ", position: " << tool.tipPosition()
			<< ", direction: " << tool.direction() << std::endl;
	}
}

void SampleListener::onFocusGained(const Controller& controller) {
	std::cout << "Focus Gained" << std::endl;
}

void SampleListener::onFocusLost(const Controller& controller) {
	std::cout << "Focus Lost" << std::endl;
}

void SampleListener::onDeviceChange(const Controller& controller) {
	std::cout << "Device Changed" << std::endl;
	const DeviceList devices = controller.devices();

	for (int i = 0; i < devices.count(); ++i) {
		std::cout << "id: " << devices[i].toString() << std::endl;
		std::cout << "  isStreaming: " << (devices[i].isStreaming() ? "true" : "false") << std::endl;
	}
}

void SampleListener::onServiceConnect(const Controller& controller) {
	std::cout << "Service Connected" << std::endl;
}

void SampleListener::onServiceDisconnect(const Controller& controller) {
	std::cout << "Service Disconnected" << std::endl;
}

int main()
{
	// Create a sample listener and controller
	SampleListener listener;
	Controller controller;

	// Have the sample listener receive events from the controller
	controller.addListener(listener);
	
	

	// Keep this process running until Enter is pressed
	std::cout << "Press Enter to quit..." << std::endl;
	std::cin.get();

	// Remove the sample listener when done
	controller.removeListener(listener);

	return 0;
}


