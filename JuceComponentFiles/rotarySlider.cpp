/*
  ==============================================================================

	THIS CODE WAS AUTOMATICALLY GENERATED

  ==============================================================================
*/

#include "../JuceLibraryCode/JuceHeader.h"
#include "not_a_real_name.h"

//==============================================================================

// >>>>INITIALISATION>>>> (auto-generated)//
// <<<<INITIALISATION<<<< (will be overwritten!!)   

// >>>>CONSTRUCTOR>>>> (auto-generated)//
// <<<<CONSTRUCTOR<<<< (will be overwritten!!)   


void not_a_real_name::drawRotarySlider(Graphics& g, int x, int y, int width, int height, float sliderPos, const float rotaryStartAngle, const float rotaryEndAngle, Slider& slider)
{
	auto bounds = Rectangle<int>(x, y, width, height).toFloat().reduced(10);
	auto radius = jmin(bounds.getWidth(), bounds.getHeight()) / 2.0f;
	auto toAngle = rotaryStartAngle + sliderPos * (rotaryEndAngle - rotaryStartAngle);
	auto lineW = jmin(8.0f, radius * 0.5f);
	auto arcRadius = radius - lineW * 0.5f;

	// >>>>PAINT>>>> (auto-generated)//
	// <<<<PAINT<<<< (will be overwritten!!)

	// >>>>RESIZED>>>> (auto-generated)//
    // <<<<RESIZED<<<< (will be overwritten!!)
}

// >>>>FUNCTION>>>> (auto-generated)//
// <<<<FUNCTION<<<< (will be overwritten!!)