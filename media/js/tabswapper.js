/*
Script: tabswapper.js
Handles the scripting for a common UI layout; the tabbed box.

Dependancies:
	mootools - 	<Moo.js>, <Utility.js>, <Function.js>, <Array.js>, <String.js>, <Element.js>, <Fx.Base.js>, <Dom.js>, <Cookie.js>
	cnet - <element.cnet.js>
	
Author:
	Aaron Newton, <aaron [dot] newton [at] cnet [dot] com>

Class: TabSwapper
		Handles the scripting for a common UI layout; the tabbed box.
		If you have a set of dom elements that are going to toggle visibility based
		on the related tabs above them (they don't have to be above, but usually are)
		you can instantiate a TabSwapper and it's handled for you.
		
		Example:
		
		><ul id="myTabs">
		>	<li><a href="1">one</a></li>
		>	<li><a href="2">two</a></li>
		>	<li><a href="3">three</a></li>
		></ul>
		><div id="myContent">
		>	<div>content 1</div>
		>	<div>content 2</div>
		>	<div>content 3</div>
		></div>
		><script>
		>	var myTabSwapper = new TabSwapper({
		>		selectedClass: "on",
		>		deselectedClass: "off",
		>		mouseoverClass: "over",
		>		mouseoutClass: "out",
		>		tabSelector: "#myTabs li",
		>		clickSelector: "#myTabs li a",
		>		sectionSelector: "#myContent div",
		>		name: "myTabSwapper",
		>		smooth: true,
		>		cookieName: "rememberMe"
		>	});
		></script>
		
		Notes:
		 - you don't have to specify the classes for mouseover/out
		 - you don't have to specify a click selector; it'll just
		   use the tab DOM elements if you don't give it the click
			 selector
		 - the click selector is NOT a subselector of the tabs; be sure
		   to specify a full css selector for these
		 - smooth: is off by default; adds some nice transitional effects
		 - cookieName: will store the users's last selected tab in a cookie
		   and restore this tab when they next visit
			 
Arguments:
	options - optional, an object containing options.

Options:
			selectedClass - the class for the tab when it is selected
			deselectedClass - the class for the tab when it isn't selected
			mouseoverClass - the class for the tab when the user mouses over
			tabSelector - the css selector to find all the tabs
			clickSelector - the css selector for all the elements the user clicks
											optional; if not defined, will use tabSelector
			sectionSelector - the css selector for the content the tabs display
			initPanel - the panel to show on init; 0 is default (optional)
			smooth - use effects to smooth transitions; false is default (optional)
			cookieName - if defined, the browser will remember their previous selection
					 	using a cookie (optional)
			cookieDays - how many days to remember this? default is 999, but it's
						ignored if cookieName isn't set (optional)
	*/

var TabSwapper = new Class({
	options: {
		selectedClass: 'tabSelected',
		mouseoverClass: 'tabOver',
		deselectedClass: '',
		tabSelector: '',
		clickSelector:'',
		sectionSelector:'',
		initPanel: 0, 
		smooth: false, 
		cookieName: null, 
		cookieDays: 999 
	},
	initialize: function(options){
		this.setOptions(options);
		this.sectionOpacities = [];
		if(!$chk(this.options.clickSelector)) this.options.clickSelector = this.options.tabSelector;
		this.setup();
		if(this.options.cookieName && this.recall()) this.swap(this.recall().toInt());
		else this.swap(this.options.initPanel);
	},
	setup: function(){
		var opt = this.options;
		$$(opt.clickSelector).each(function(lnk, idx){
			lnk.addEvent('click', function(){this.swap(idx)}.bind(this));
		},this);
		this.tabs = $$(opt.tabSelector);
		this.sections = $$(opt.sectionSelector);
		this.tabs.each(function(tab, i){
			tab.addEvent('mouseout',function(){
				tab.removeClass(this.options.mouseoverClass);
			}.bind(this)).addEvent('mouseover', function(){
				tab.addClass(this.options.mouseoverClass);
			}.bind(this));
		}.bind(this));
	},
	swap: function(swapIdx){
		this.sections.each(function(sect, idx){
			if(swapIdx == idx) this.showSection(idx);
			else this.hideSection(idx);
		}, this);
		if(this.options.cookieName) this.save(swapIdx);
	},
	save: function(index){
		Cookie.set(this.options.cookieName, index, {duration:this.options.cookieDays});
	},
	recall: function(){
		return $pick(Cookie.get(this.options.cookieName), false);
	},
	hideSection: function(idx) {
		this.sections[idx].hide();
		this.tabs[idx].removeClass(this.options.selectedClass).addClass(this.options.deselectedClass);
	},
	showSection: function(idx) {
		var sect = this.sections[idx];
		if(!sect.visible()) {
			if (!this.sectionOpacities[idx]) this.sectionOpacities[idx] = this.sections[idx].effect('opacity', {duration: 500});
			sect.show();
			if(this.options.smooth && (!window.ie6 || (window.ie6 && sect.fxOpacityOk()))) this.sectionOpacities[idx].custom(0,1);
			else if(sect.getStyle('opacity') < 1) this.sectionOpacities[idx].set(1);
		}
		this.tabs[idx].addClass(this.options.selectedClass).removeClass(this.options.deselectedClass);
	}
});
TabSwapper.implement(new Options);
//legacy namespace
var tabSwapper = TabSwapper;
/* do not edit below this line */   
/* Section: Change Log 

$Source: /cvs/main/flatfile/html/rb/js/global/cnet.global.framework/common/layout.widgets/tabswapper.js,v $
$Log: tabswapper.js,v $
Revision 1.10  2007/04/12 23:47:34  newtona
fixed a bug where if you defined tabSelector but not clickSelector, things went whacky; now it acts as it should - if !clickSelector then clickSelector = tabSelector

Revision 1.9  2007/03/28 18:08:35  newtona
tabswapper now uses Element.fxOpacityOk to deal with the IE bug where text gets blurry when you fade an element in and out without a bgcolor set

Revision 1.8  2007/03/23 17:59:39  newtona
tabswapper no longer cmplains about this.recall() on load

Revision 1.7  2007/03/16 17:18:41  newtona
transitions no longer used for ie6

Revision 1.6  2007/02/27 19:40:42  newtona
enforcing element.show to use display block

Revision 1.5  2007/02/07 20:51:55  newtona
implemented Options class
implemented Events class

Revision 1.4  2007/01/26 05:53:33  newtona
syntax update for mootools 1.0
docs update
renamed tabSwapper - > TabSwapper

Revision 1.3  2007/01/22 22:49:48  newtona
updated cookie.set syntax

Revision 1.2  2007/01/22 21:59:19  newtona
updated for mootools 1.0

Revision 1.1  2007/01/09 02:39:35  newtona
renamed addons directory to "common" directory

Revision 1.4  2007/01/09 01:26:49  newtona
changed $S to $$

Revision 1.3  2006/11/21 23:55:56  newtona
optimization update

Revision 1.2  2006/11/02 21:26:42  newtona
checking in commerce release version of global framework.

notable changes here:
cnet.functions.js is the only file really modified, the rest are just getting cvs footers (again).

cnet.functions adds numerous new classes:

$type.isNumber
$type.isSet
$set

*/