# FUI File Structure Documentation
## Base Information
FUI Files are Mojangs/4J's way of storing Game UI Assets.

*FUI files use the LSB(Little Endian) byte order.*

The following Table gives you Important information about each structure that can be represented in a FUI file:
| Name | Size (per element) | Description |
| :-:|:-:|:-:|
| fuiHeader | 0x98 | Header Information (only exists once in each FUI file, always at offset 0)
| fuiTimeline | 0x1c | 
| fuiTimelineAction | 0x84 | 
| fuiShape | 0x1c | 
| fuiShapeComponent | 0x2c | 
| fuiVert | 0x8 | 2D float Vertex
| fuiTimelineFrame | 0x48 | 
| fuiTimelineEvent | 0x48 | 
| fuiTimelineEventName | 0x40 | Name for a given event
| fuiReference | 0x48 | Reference to Symbols in Imported Assests(Files)
| fuiEdittext | 0x138 | 
| fuiFontName | 0x104 | 
| fuiSymbol | 0x48 | Defined Symbols with Name and Object type (entry point for objects used in-game)
| fuiImportAsset | 0x40 | file name to import references from
| fuiBitmap | 0x20 | Information about an Image contained in the file

### Used structures in an FUI element
These structures are used in some Elements in an FUI file
| Name | Byte Size | Description |
| :-:|:-:|:-:|
| fuiRect | 0x10 | A Representation of a Rectangle
| fuiRGBA | 0x4 | Base Color format used in FUI files
| fuiMatrix | 0x18 | 2D Matrix for Scale, Rotation and Translation
| fuiColorTransform | 0x20 | 
| fuiFillStyle | 0x24 | Contains Information for filling
| fuiObject.eFuiObjectType | 0x4 | Describes the Type of an Element

## fuiRect

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Min. X | 0x0 | 4 | float | Minimun X position
| Max. X | 0x4 | 4 | float | Maximun X position
| Min. Y | 0x8 | 4 | float | Minimun Y position
| Max. Y | 0xc | 4 | float | Maximun Y position

## fuiRGBA

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Color | 0x0 | 4 | int | 8-bit Color in RGBA byte order

## fuiMatrix

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Scale X | 0x0 | 4 | float | 
| Scale Y | 0x4 | 4 | float | 
| Rotate Skew 0 | 0x8 | 4 | float | 
| Rotate Skew 1 | 0xc | 4 | float | 
| Translate X | 0x10 | 4 | float | 
| Translate Y | 0x14 | 4 | float | 

## fuiColorTransform
This is Untested just referenced by the .swf file docs!!\

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| RedMultTerm | 0x0 | 4 | float | 
| GrennMultTerm | 0x4 | 4 | float | 
| BlueMultTerm | 0x8 | 4 | float | 
| AlphaMultTerm | 0xc | 4 | float | 
| RedAddTerm | 0x10 | 4 | float | 
| GrennAddTerm | 0x14 | 4 | float | 
| BlueAddTerm | 0x18 | 4 | float | 
| AlphaAddTerm | 0x1c | 4 | float | 

## fuiFillStyle

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Type/Operation | 0x0 | 4 | int | wheather to use a bitmap or fill area with a given color
| Color | 0x4 | 4 | fuiRGBA | color to use when filling area
| Bitmap Index | 0x8 | 4 | int | Index of the bitmap to use
| Matrix | 0xc | 0x18 | fuiMatrix | matrix for area ?


## FUI Header

**The FUI file Header is the most crucial part of an fui file it holds infomation for
allocating memory at runtime, counts of fui Objects and is part of the in-game `fuifile` class**

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Signature | 0x0 | 8 | char[] | FUI File Signature (b'\x01IUF\x00\x00\x00\x00') where (\x01) indecates the version of the fui file
| Content Size | 0x8 | 4 | int | Size of the up coming data in the FUI file
| Swf File Name | 0xc | 0x40 | char[] | Name used to import file
| fuiTimeline Count | 0x4c | 4 | int | Count of fuiTimeline Elements in a file
| fuiTimelineEventName Count | 0x50 | 4 | int | Count of fuiTimelineEventName Elements in a file
| fuiTimelineAction Count | 0x54 | 4 | int | Count of fuiTimelineAction Elements in a file
| fuiShape Count | 0x58 | 4 | int | Count of fuiShape Elements in a file
| fuiShapeComponent Count | 0x5c | 4 | int | Count of fuiShapeComponent Elements in a file
| fuiVert Count | 0x60 | 4 | int | Count of fuiVert Elements in a file
| fuiTimelineFrame Count | 0x64 | 4 | int | Count of fuiTimelineFrame Elements in a file
| fuiTimelineEvent Count | 0x68 | 4 | int | Count of fuiTimelineEvent Elements in a file
| fuiReference Count | 0x6c | 4 | int | Count of fuiReference Elements in a file
| fuiEdittext Count | 0x70 | 4 | int | Count of fuiEdittext Elements in a file
| fuiSymbol Count | 0x74 | 4 | int | Count of fuiSymbol Elements in a file
| fuiBitmap Count | 0x78 | 4 | int | Count of fuiBitmap Elements in a file
| images size | 0x7c | 4 | int | Size of all Images in the file
| fuiFontName Count | 0x80 | 4 | int | Count of fuiFontName Elements in a file
| fuiImportAsset Count | 0x84 | 4 | int | Count of fuiImportAsset Elements in a file
| Frame Size | 0x88 | 0x10 | fuiRect | Size of the frame ?

## fuiTimeline
| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Symbol Index | 0x0 | 4 | int | Index of the symbol to use. -1 if it has no symbol linked.
| Frame Index | 0x4 | 2 | short | Index in fuiTimelineFrame array
| Frame Count | 0x6 | 2 | short | Count of how many fuiTimelineFrame's are used
| Action Index | 0x8 | 2 | short | Index in fuiTimelineAction array
| Action Count | 0xa | 2 | short | Count of how many fuiTimelineAction's are used
| Rectangle | 0xc | 0x10 | fuiRect | Unknown fuiRect

## fuiTimelineAction

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Action Type | 0x0 | 2 | short | action to make
| Unknown | 0x2 | 2 | short | Probably Value Arg0 for specific Action types
| String Arg 0 | 0x4 | 0x40 | char[] | 
| String Arg 1 | 0x44 | 0x40 | char[] | 


## fuiShape

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Unknown | 0x0 | 4 | int | 
| Shape Component Index | 0x4 | 4 | int | 
| Shape Component Count | 0x8 | 4 | int | 
| Rectangle | 0xc | 0x10 | fuiRect | Size of th given Shape(Component)

## fuiShapeComponent

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Fill Info | 0x0 | 0x24 | fuiFillStyle | Component Fill Info
| Vert Index | 0x24 | 4 | int | 
| Vert Count | 0x28 | 4 | int | 

## fuiVert

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| X | 0x0 | 4 | float | X Position of the Vertex
| Y | 0x4 | 4 | float | Y Position of the Vertex

## fuiTimelineFrame

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Frame Name | 0x0 | 0x40 | char[] | Name of the Frame
| Event Index | 0x40 | 4 | int | Index to start from fuiTimelineEvent
| Event Count | 0x44 | 4 | int | Count of fuiTimelineEvents that get used

## fuiTimelineEvent

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Event Type | 0x0 | 0x2 | short | 
| Object Type | 0x2 | 0x2 | short | 
| Unknown | 0x4 | 0x2 | short | 
| Index | 0x6 | 0x2 | short | 
| Unknown | 0x8 | 0x2 | short | 
| Name Index | 0xa | 0x2 | short | 
| matrix | 0xc | 0x18 | fuiMatrix | 
| ColorTransform | 0x24 | 0x20 | fuiColorTransform | Useless
| Color | 0x44 | 4 | fuiRGBA |

## fuiTimelineEventName

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Event Name | 0x0 | 0x40 | char[] | Name of the Timeline Event

## fuiReference

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Symbol Index | 0x0 | 4 | int | Index of Symbol (resolved at runtime)
| Name | 0x4 | 0x40 | char[] | Reference to a Symbol that is contained in an Import file
| Index | 0x44 | 4 | int | fuiFile Index (resolved at runtime)

## fuiEdittext

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Unknown | 0x0 | 4 | int | 
| rectangle | 0x4 | 0x10 | fuiRect | 
| Font Id | 0x14 | 4 | int | 
| Unknown | 0x18 | 4 | float | 
| Color | 0x1c | 4 | fuiRGBA | 
| Unknown | 0x20 | 0x18 | int | 6 unknwon int
| Html text | 0x38 | 0x100 | char[] | 

## fuiFontName

TODO: get proper names and types!

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Id | 0x0 | 4 | int | 
| Font Name | 0x4 | 0x40 | char[] | Name of the Font
| Unknown | 0x44 | 4 | int | 
| Unknown | 0x48 | 0x40 | char[] | 
| Unknown | 0x88 | 8 | int | 2 Unknown ints
| Unknown | 0x90 | 0x40 | char[] | 
| Unknown | 0xd0 | 8 | int | 2 Unknown ints
| Unknown | 0xd8 | 0x2c | char[] | 

## fuiSymbol

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Symbol Name | 0x0 | 0x40 | char[] | Name of the Symbol
| Object Type | 0x40 | 4 | int | Symbols can only have two types (2 = Timeline, 3 = Bitmap)
| Index | 0x44 | 4 | int | Index mapped to the object type list

## fuiImportAsset

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Name | 0x0 | 0x40 | char[] | File Name to import from

## fuiBitmap

**Important**: _PNG files use BGRA instead of RGBA!_

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Unknown | 0x0 | 4 | int | Could be some kind of id
| Image Format | 0x4 | 4 | int | Format to use ([see fuiBitmap](./python/fuiDataStructures/fuiBitmap.py))
| Width | 0x8 | 4 | int | Width of the given Image (possiblly used for memory allocation)
| Height | 0xc | 4 | int | Height of the given Image (possiblly used for memory allocation)
| Offset | 0x10 | 4 | int | Offset of the Image
| Size | 0x14 | 4 | int | Size of the image
| Zlib Data Offset | 0x18 | 4 | int | zlib data start offset (only set when using `JPEG_WITH_ALPHA_DATA`)
| Unknown | 0x1c | 4 | int | -1 if something failed at runtime
