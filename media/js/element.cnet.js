/*	Script: element.cnet.js
Extends the <Element> object.

Dependancies:
	 mootools - <Moo.js>, <String.js>, <Array.js>, <Function.js>, <Element.js>, <Dom.js>

Author:
	Aaron Newton, <aaron [dot] newton [at] cnet [dot] com>
	
Class: Element
		This extends the <Element> prototype.
	*/
Element.extend({
/*	Property: getDimensions
		Returns width and height for element; if element is not visible the element is
		cloned off screen, shown, measured, and then removed.
		
		Arguments:
		options - a key/value set of options
		
		Options:
		computeSize - (boolean; optional) use <Element.getComputedSize> or not; defaults to false
		styles - (array; optional) see <Element.getComputedSize>
		plains - (array; optional) see <Element.getComputedSize>
		
		Returns:
		An object with .width and .height defined as integers. If options.computeSize is true, returns
		all the values that <Element.getComputedSize> returns.
		
		Example:
		>$(id).getDimensions()
		> > {width: #, height: #}
	*/
	getDimensions: function(options) {
		options = $merge({computeSize: false},options);
		var dim = {};
		function getSize(el, options){
			if(options.computeSize) dim = el.getComputedSize(options);
			else {
				dim.width = el.getSize().size.x;
				dim.height = el.getSize().size.y;
			}
			return dim;
		}
		try { //safari sometimes crashes here, so catch it
			dim = getSize(this, options);
		}catch(e){}
		if((dim.x == 0 || $type(dim.x) != 'number')||(dim.y == 0 || $type(dim.y) != 'number')){
			var holder = new Element('div').setStyles({
				'position':'absolute',
				'top':'-1000px',
				'left':'-1000px',
				'display':'block'
			}).injectAfter(this);
			var clone = this.clone().injectInside(holder).show();
			dim = getSize(clone, options);
			holder.remove();
		}
		return $merge(dim, {x: dim.width, y: dim.height});
	},
/*	Property: getComputedSize
		Calculates the size of an element including the width, border, padding, etc.
		
		Arguments:
		options - an object with key/value options
		
		Options:
		styles - (array) the styles to include in the calculation; defaults to ['padding','border']	
		plains - (object) an object with height and width properties, each of which is an 
							array including the edges to include in that plain. 
							defaults to {height: ['top','bottom'], width: ['left','right']}
		mode - (string; optional) limit the plain to 'vertical' or 'horizontal'; defaults to 'both'
		
		Returns:
		size - an object that contans dimension values (integers); see list below
		
		
		Dimension Values Returned:
		width - the actual width of the object (not including borders or padding)
		height - the actual height of the object (not including borders or padding)
		border-*-width - (where * is top, right, bottom, and left) the width of the border on that edge
		padding-* - (where * is top, right, bottom, and left) the width of the padding on that edge
		computed* - (where * is Top, Right, Bottom, and Left; e.g. computedRight) the width of all the 
			styles on that edge computed (so if options.styles is left to the default padding and border,
			computedRight is the sum of border-right-width and padding-right)
		totalHeight - the total sum of the height plus all the computed styles on the top or bottom. by
			default this is just padding and border, but if you were to specify in the styles option
			margin, for instance, the totalHeight calculated would include the margin.
		totalWidth - same as totalHeight, only using width, left, and right
	*/
	getComputedSize: function(options){
		options = $merge({
			styles: ['padding','border'],
			plains: {height: ['top','bottom'], width: ['left','right']},
			mode: 'both'
		}, options);
		var size = {width: 0,height: 0};
		switch (options.mode){
			case 'vertical':
				delete size.width;
				delete options.plains.width;
				break;
			case 'horizontal':
				delete size.height;
				delete options.plains.height;
				break;
		}
		var getStyles = [];
		//this function might be useful in other places; perhaps it should be outside this function?
		$each(options.plains, function(plain, key){
			plain.each(function(edge){
				options.styles.each(function(style){
					getStyles.push((style=="border")?style+'-'+edge+'-'+'width':style+'-'+edge);
				});
			});
		});
		var styles = this.getStyles.apply(this, getStyles);
		var subtracted = [];
		$each(options.plains, function(plain, key){ //keys: width, height, plains: ['left','right'], ['top','bottom']
			size['total'+key.capitalize()] = 0;
			size['computed'+key.capitalize()] = 0;
			plain.each(function(edge){ //top, left, right, bottom
				size['computed'+edge.capitalize()] = 0;
				getStyles.each(function(style,i){ //padding, border, etc.
					//'padding-left'.test('left') size['totalWidth'] = size['width']+[padding-left]
					if(style.test(edge)) {
						styles[style] = styles[style].toInt(); //styles['padding-left'] = 5;
						if(isNaN(styles[style]))styles[style]=0;
						size['total'+key.capitalize()] = size['total'+key.capitalize()]+styles[style];
						size['computed'+edge.capitalize()] = size['computed'+edge.capitalize()]+styles[style];
					}
					//if width != width (so, padding-left, for instance), then subtract that from the total
					if(style.test(edge) && key!=style && 
						(style.test('border') || style.test('padding')) && !subtracted.test(style)) {
						subtracted.push(style);
						size['computed'+key.capitalize()] = size['computed'+key.capitalize()]-styles[style];
					}
				});
			});
		});
		if($chk(size.width)) {
			size.width = size.width+this.offsetWidth+size.computedWidth;
			size.totalWidth = size.width + size.totalWidth;
			delete size.computedWidth;
		}
		if($chk(size.height)) {
			size.height = size.height+this.offsetHeight+size.computedHeight;
			size.totalHeight = size.height + size.totalHeight;
			delete size.computedHeight;
		}
		return $merge(styles, size);
	},
/*	Property: setPosition
		Sets the location of an element relative to another (defaults to the document body).
		
		Note:
		The element must be absolutely positioned (if it isn't, this method will set it to be);
		
		Arguments:
		options - a key/value object with options
		
		Options:
		relativeTo - (element) the element relative to which to position this one; defaults to document.body.
		position - (string) the aspect of the relativeTo element that this element should be positioned. Options are 'upperRight', 'upperLeft', 'bottomLeft', 'bottomRight', and 'center' (the default). With the exception of center, all other options will make the upper right corner of the positioned element = the specified corner of the relativeTo element. 'center' will make the center point of the positioned element = the center point of the relativeTo element.
		edge - (string; optional) the edge of the element to set relative to the relative elements corner; this way you can specify to position this element's upper right corner to the bottom left corner of the relative element. this is optional; the default behavior positions the element's upper left corner to the relative element unless position == center, in which case it positions the center of the element to the center of the relative element.
		offset - (object) x/y coordinates for the offset (i.e. {x: 10, y:100} will move it down 100 and to the right 10). Negative values are allowed.
		smoothMove - (boolean) move the element to the new position using <Fx.Styles>; defaults to false.
		effectOptions - (object) options object for <Fx.Styles>, optional
		returnPos - (boolean) don't move the element, but instead just return the position object ({top: '#', left: '#'}); defaults to false
		
		Example:
(start code)
$(el).getComputedSize();
returns:
{
	padding-top:0,
	border-top-width:1,
	padding-bottom:0,
	border-bottom-width:1,
	padding-left:0,
	border-left-width:1,
	padding-right:0,
	border-right-width:1,
	width:100,
	height:100,
	totalHeight:102,
	computedTop:1,
	computedBottom:1,
	totalWidth:102,
	computedLeft:1,
	computedRight:1
}
(end)		
	*/
	setPosition: function(options){
		options = $merge({
			relativeTo: document.body,
			position: 'center',
			edge: false,
			offset: {x:0,y:0},
			smoothMove: false,
			effectOptions: {},
			returnPos: false
		}, options);
		this.setStyle('position', 'absolute');
		var rel = $(options.relativeTo) || document.body;
		var top = (rel == document.body)?window.getScrollTop():rel.getTop();
		if (top < 0) top = 0;
		var left = (rel == document.body)?window.getScrollLeft():rel.getLeft();
		if (left < 0) left = 0;
		var dim = this.getDimensions({computeSize: true});
		var pos;
		var prefY = options.offset.y.toInt();
		var prefX = options.offset.x.toInt();
		switch(options.position) {
			case 'upperLeft':
				pos = {
					x:(left + prefX),
					y:(top + prefY)
				};
				break;
			case 'upperRight':
				pos = {
					x:(left + prefX + rel.offsetWidth),
					y:(top + prefY)
				};
				break;
			case 'bottomLeft':
				pos = {
					x:(left + prefX),
					y:(top + prefY + rel.offsetHeight)
				};
				break;
			case 'bottomRight':
				pos = {
					y:(left + prefX + rel.offsetWidth),
					x:(top + prefY + rel.offsetHeight)
				};
				break;
			default: //center
				pos = {
					x: left + (((rel == document.body)?window.getWidth():rel.offsetWidth)/2) + prefX,
					y: top + (((rel == document.body)?window.getHeight():rel.offsetHeight)/2) + prefY
				};
				options.edge = "center";
				break;
		}
		if(options.edge){
			var edgeOffset;
			switch(options.edge){
				case 'upperLeft':
					edgeOffset = {
						x: 0,
						y: 0
					};
					break;
				case 'upperRight':
					edgeOffset = {
						x: -dim.x-dim.computedRight-dim.computedLeft,
						y: 0
					};
					break;
				case 'bottomLeft':
					edgeOffset = {
						x: 0,
						y: -dim.y-dim.computedTop-dim.computedBottom
					};
					break;
				case 'bottomRight':
					edgeOffset = {
						x: -dim.x-dim.computedRight-dim.computedLeft,
						y: -dim.y-dim.computedTop-dim.computedBottom
					};
					break;
				default: //center
					edgeOffset = {
						x: -(dim.x/2),
						y: -(dim.y/2)
					};
					break;
			}
			pos.x = pos.x+edgeOffset.x;
			pos.y = pos.y+edgeOffset.y;
		}
		pos = {
			left: ((pos.x >= 0)?pos.x:0).toInt()+'px',
			top: ((pos.y >= 0)?pos.y:0).toInt()+'px'
		};
		if(options.returnPos) return pos;
		if(options.smoothMove && this.effects) this.effects(options.effectOptions).start(pos);
		else this.setStyles(pos);
		return this;
	},

/*	Property: visible
		Returns a boolean; true = visible, false = not visible.
		
		Example:
		>$(id).visible()
		> > true | false	*/
	visible: function() {
		return this.getStyle('display') != 'none';
	},
/*	Property: toggle
		Toggles the state of an element from hidden (display = none) to 
		visible (display = what it was previously or else display = block)
		
		Example:
		> $(id).toggle()
	*/
	toggle: function() {
		return this[this.visible() ? 'hide' : 'show']();
	},
/*	Property: hide
		Hides an element (display = none)
		
		Example:
		> $(id).hide()
		*/
	hide: function() {
		this.originalDisplay = this.getStyle('display'); 
		this.setStyle('display','none');
		return this;
	},
/*	Property: smoothHide
		Transitions the height, opacity, padding, and margin (but not border) from their current height to zero, then set's display to none and resets the height, opacity, etc. back to their original values.

		Arguments:
		options - a key/value object of options
		
		Options:
		all the options passed along to <Fx.Base> (transition, duration, etc.); (optional); PLUS
		styles - (array; optional) css properties to transition in addition to width/height; 
							defaults to ['padding','border','margin']
		mode - (string; optional) 'vertical','horizontal', or 'both' to describe how the element should slide in.
							defaults to 'vertical'
	*/
	smoothHide: function(options){
		options = $merge({
			styles: ['padding','border','margin'],
			mode:'vertical'
		},options);
		function fixStyle(style, name){
			if(!$type(style)=="number") return style;
			var fix = ['margin', 'padding', 'width', 'height'].some(function(st){return name.test(st, 'i')});
			return (fix)?style+'px':style;
		}
		if(this.getStyle('display') != 'none'){
			var startStyles = this.getComputedSize({
				styles: options.styles,
				mode: options.mode
			});
			if (this.fxOpacityOk()) startStyles.opacity = 1;
			var zero = {};
			$each(startStyles, function(style, name){
				zero[name] = fixStyle(0, name); 
			});
			this.effects(options).start(zero).chain(function(){
				$each(startStyles, function(style, name) {
					startStyles[name] = fixStyle(style, name);
				});
				this.setStyles(startStyles).setStyle('display','none');
			}.bind(this));
		}
		return this;
	},
/*	Property: smoothShow
		Sets the display of the element to opacity: 0 and display: block, then transitions the height, opacity, padding, and margin (but not border) from zero to their proper height.
		
		Arguments:
		all the options passed along to <Fx.Base> (transition, duration, etc.); (optional); PLUS
		mode - (string; optional) 'vertical','horizontal', or 'both' to describe how the element should slide in.
		heightOverride - (integer; optional) height to open to; overrides the default offsetheight
		widthOverride -  (integer; optional) width to open to; overrides the default offsetwidth
	*/
	smoothShow: function(options){
		if(arguments[1]) options.heightOverride = arguments[1];
		options = $merge({
			styles: ['padding','border','margin'],
			mode: 'vertical'
		}, options);
		function fixStyle(style, name){
			if(!$type(style)=="number") return style;
			var fix = ['margin', 'padding', 'width', 'height'].some(function(st){return name.test(st, 'i')});
			return (fix)?style+'px':style;
		}
		if(this.getStyle('display') == "none" || 
			 this.getStyle('visiblity') == "hidden" || 
			 this.getStyle('opacity')==0){
			//toggle display, but hide it
			this.setStyle('display','block');
			if(this.fxOpacityOk()) this.setStyle('opacity',0);
			var startStyles = this.getComputedSize({
				styles: options.styles,
				mode: options.mode
			});
			$each(startStyles, function(style, name) {
				startStyles[name] = fixStyle(style, name);;
			});
			if(this.fxOpacityOk()) startStyles.opacity = 1;
			var zero = { height: '0px' };
			$each(startStyles, function(style, name){ zero[name] = fixStyle(0, name); });
			this.setStyles(zero).effects(options).start(startStyles);
		}
		return this;
	},
/*	Property: show
		Shows an element (display = what it was previously or else display = block)
		
		Example:
		>$(id).show() */
	show: function(display) {
		this.originalDisplay = (this.originalDisplay=="none")?'block':this.originalDisplay;
		this.setStyle('display',(display || this.originalDisplay || 'block'));
		return this;
	},
/*	Property: cleanWhitespace
		Removes all empty text nodes from an element and its children
		
		Example:
		> $(id).cleanWhitespace()	*/
	cleanWhitespace: function() {
		$A(this.childNodes).each(function(node){
			if (node.nodeType == 3 && !/\S/.test(node.nodeValue)) node.parentNode.removeChild(node);
		});
		return this;
	},
/*	Property: find
		Returns an element from the node's array (such as parentNode), deprecated (left over from Prototype.lite).
		
		Arguments:
		what - the value you wish to find (such as 'parentNode')

		Example:
		> $(id).find(parentNode)
	*/
	find: function(what) {
		var element = this[what];
		while (element.nodeType != 1) element = element[what];
		return element;
	},
/*	Property: replace
		Replaces an html element with the html passed in.
		
		Arguments:
		html - the html with which to replace the node.
		evalScripts - (boolean; optional) evaluate javascript in the new node. defaults to true.
		
		Example:
		>$(id).replace(myHTML) */
	replace: function(html, evalScripts) {
		if (this.outerHTML) {
			this.outerHTML = html.stripScripts();
		} else {
			var range = this.ownerDocument.createRange();
			range.selectNodeContents(this);
			this.parentNode.replaceChild(
				range.createContextualFragment(html.stripScripts()), this);
		}
		if($pick(evalScripts, true)) html.evalScripts.delay(10, html);
	},
/*	Property: empty
		Returns a boolean: true = the Node is empty, false, it isn't.
		
		Example:
		> $(id).empty
		> true (the node is empty) | false (the node is not empty)
	*/
	isEmpty: function() {
		return !!this.innerHTML.match(/^\s*$/);
	},
	/*	Property: getOffsetHeight
			Returns the offset height of an element, deprecated.
			You should instead use <Element.getStyle>('height')
			or just Element.offsetHeight.
			
			Example:
			> $(id).getOffsetHeight()
		*/
	getOffsetHeight: function(){ return this.offsetWidth; },
	/*	Property: getOffsetWidth
			Returns the offset width of an element, deprecated.
			You should instead use <Element.getStyle>('width')
			or just Element.offsetWidth.
			
			Example:
			> $(id).getOffsetWidth()
		*/
	getOffsetWidth: function(){ return this.offsetWidth; },
/*	Property: tidy
		Uses <String.tidy> to clean up common special characters with their ASCII counterparts (smart quotes, elipse characters, stuff from MS Word, etc.).
	*/
	tidy: function(){
		try {	
			if(this.getValue().tidy())this.value = this.getValue().tidy();
		}catch(e){dbug.log('element.tidy error: %o', e);}
	},
	//DO NOT USE THIS METHOD
	//it is temporary, as Mootools 1.1 will negate its requirement
	fxOpacityOk: function(){
		if (!window.ie6)return true;
		var isColor = false;
		try {
			if (new Color(this.getStyle('backgroundColor'))) isColor = true;
		}catch(e){}
		return isColor;
	}
});


if(!Element.empty) {
	Element.extend({
		/*
		Property: empty
			Empties an element of all its children.
	
		Example:
			>$('myDiv').empty() // empties the Div and returns it
	
		Returns:
			The element.
		*/
		empty: function(){
			//Garbage.trash(this.getElementsByTagName('*'));
			return this.setHTML('');
		}
	});
}
/*	legacy support for $S	*/
var $S = $$;
/* do not edit below this line */   
/* Section: Change Log 

$Source: /cvs/main/flatfile/html/rb/js/global/cnet.global.framework/mootools.extended/element.cnet.js,v $
$Log: element.cnet.js,v $
Revision 1.29  2007/05/17 19:45:57  newtona
updated element.empty for mootools 1.1

Revision 1.28  2007/05/16 20:09:42  newtona
adding new js files to redball.common.full
product.picker.js now has no picklets; these are in the implementations/picklets directory
ProductPicker now detects if there is no doctyp and, if not, sets the position of the picker to be fixed (no IE6 support)
small docs update in element.cnet.js
added new picklet: CNETProductPicker_PricePath
added new picklet: NewsStoryPicker_Path
new file: clipboard.js (allows you to insert text into the OS clipboard)
new file: html.table.js (automates building html tables)
new file: element.forms.js (for managing text inputs - get selected text information, insert content around selection, etc.)

Revision 1.27  2007/05/05 01:01:26  newtona
stickywinHTML: tweaked the options for buttons
element.cnet: tweaked smoothshow/hide css handling

Revision 1.26  2007/04/09 21:35:22  newtona
removing garbage collection from Element.empty (will have to wait for Mootools 1.1)

Revision 1.25  2007/04/02 18:04:48  newtona
syntax fix

Revision 1.24  2007/03/30 21:42:43  newtona
adding Element.isEmpty

Revision 1.23  2007/03/30 19:27:58  newtona
moved .empty to .flush

Revision 1.22  2007/03/29 22:36:42  newtona
Element.fxOpacityOk now only checks bgcolor for ie6
Added Element.flush

Revision 1.21  2007/03/28 23:22:54  newtona
Element.smoothShow/smoothHide: added Element.fxOpacityOk to deal with the IE bug where text gets blurry when you fade an element in and out without a bgcolor set

Revision 1.20  2007/03/28 18:07:21  newtona
added Element.fxOpacityOk to deal with the IE bug where text gets blurry when you fade an element in and out without a bgcolor set

Revision 1.19  2007/03/26 18:30:12  newtona
iframeShim: fixed reference to options (should be this.options)
element.cnet: removed some dbug lines

Revision 1.18  2007/03/23 20:13:38  newtona
getDimensions: added support for getComputedSize
getComputedSize: added
setPosition: added edge option, uses getComputedSize
smoothHide: uses getComputedSize
smoothShow: uses getComputedSize
sumObj: removed function; no longer needed

Revision 1.17  2007/03/16 00:23:24  newtona
added string.tidy and element.tidy

Revision 1.16  2007/03/08 23:32:14  newtona
strict javascript warnings cleaned up

Revision 1.15  2007/03/01 00:50:35  newtona
type.isNumber now returns false for NaN
element.smoothshow/hide now works (in IE specifically) when there are no values for border

Revision 1.14  2007/02/27 19:37:56  newtona
element.show now enforces that the original display was not 'none'

Revision 1.13  2007/02/22 21:05:35  newtona
smoothHide now checks that the element is not already hidden

Revision 1.12  2007/02/21 00:21:22  newtona
added legacy support for $S

Revision 1.11  2007/02/08 22:14:04  newtona
added border widths to smoothshow/hide

Revision 1.10  2007/02/08 01:30:58  newtona
tweaking element.setPosition, now can use effects

Revision 1.9  2007/02/07 20:52:34  newtona
added Element.position

Revision 1.8  2007/02/06 18:13:13  newtona
added element.smoothShow and smoothHide; depends on latest svn of mootools

Revision 1.7  2007/02/03 01:40:05  newtona
fixed a typo bug

Revision 1.6  2007/01/26 06:06:13  newtona
element.replace now takes a 2nd argument to eval scripts or not
element.getDimensions now returns w & h for hidden elements

Revision 1.5  2007/01/05 19:45:48  newtona
made getDimensions capable of discovering dimensions of hidden elements

Revision 1.4  2006/12/06 20:14:59  newtona
carousel - improved performance, changed some syntax, actually deployed into usage and tested
cnet.nav.accordion - improved css selectors for time
multiple accordion - fixed a typo
dbug.js - added load timers
element.cnet.js - changed syntax to utilize mootools more effectively
function.cnet.js - equated $set to $pick in preparation for mootools v1

Revision 1.3  2006/11/27 17:59:32  newtona
small change to replace and the way it uses timeouts

Revision 1.2  2006/11/02 21:34:00  newtona
Added cvs footer


*/
