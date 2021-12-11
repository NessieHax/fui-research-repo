# FUI File Structure Documentation
## Base Information
FUI Files are Mojangs/4J's way of storing Game UI Assets.

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
| fuiTimelineEventName | 0x40 | 
| fuiReference | 0x48 | Reference to other Symbols
| fuiEdittext | 0x138 | 
| fuiFontName | 0x104 | 
| fuiSymbol | 0x48 | Defined Symbols with Name and Object type
| fuiImportAsset | 0x40 | Assests Imports form other .swf/.fui files
| fuiBitmap | 0x20 | Base Information about an Image/Shape contained in the file

Most data in a FUI structure uses the LSB(Little Endian) byte order.

### Used structures in an FUI element
These structures are used in some Elements in an FUI file
| Name | Byte Size | Description |
| :-:|:-:|:-:|
| fuiRect | 0x10 | A Representation of a Rectangle
| fuiRGBA | 0x4 | Base Color format used in FUI
| fuiMatrix | 0x18 | 
| fuiColorTransform | 0x20 | 
| fuiFillStyle | 0x24 | Contains Information for filling 
| fuiObject.eFuiObjectType | 0x4 | Describes the Type of some Elements

## fuiRect

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| X (min X) | 0x0 | 4 | float | Minimun X position of the Rectangle
| Width (max X) | 0x4 | 4 | float | Maximun X position of the Rectangle
| Y (min Y) | 0x8 | 4 | float | Minimun Y position of the Rectangle
| Height (max Y) | 0xc | 4 | float | Maximun Y position of the Rectangle

## fuiRGBA

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Color | 0x0 | 4 | int | Hex Color in RGBA byte order

## fuiMatrix
This is Untested just referenced by the .swf file docs!!

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
This Might also be [`Color transform with alpha record` (page 25)](https://www.adobe.com/content/dam/acom/en/devnet/pdf/swf-file-format-spec.pdf).

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| HasAddTerm | 0x0 | 4 | bool | 
| HasMultTerm | 0x4 | 4 | bool | 
| RedMultTerm | 0x8 | 4 | float | 
| GrennMultTerm | 0xc | 4 | float | 
| BlueMultTerm | 0x10 | 4 | float | 
| RedAddTerm | 0x14 | 4 | float | 
| GrennAddTerm | 0x18 | 4 | float | 
| BlueAddTerm | 0x1c | 4 | float | 

## fuiFillStyle
This is Untested just referenced by the .swf file docs!!

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Unknown | 0x0 | 4 | int | 
| Color | 0x4 | 4 | fuiRGBA | 
| Unknown | 0x8 | 4 | int | 
| Matrix | 0xc | 0x18 | fuiMatrix | 


## FUI Header
The Table below describes all members of the FUI Header:

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Identifier | 0x0 | 4 | char[] | FUI Header Magic (b'\x01IUF') first value (\x01) indecates the version of the fui file
| Unknow | 0x4 | 4 | int | Unknow Value
| Content Size | 0x8 | 4 | int | Size of the up coming data in the FUI file
| Swf File Name | 0xc | 0x40 | char[] | Name of the .swf file
| fuiTimeline Count | 0x4c | 4 | int | Count of fuiTimeline Elements in a file
| fuiTimelineEventName Count | 0x50 | 4 | int | Count of fuiTimelineEventName Elements in a file
| fuiTimelineAction Count | 0x54 | 4 | int | Count of fuiTimelineAction Elements in a file
| fuiShape  Count | 0x58 | 4 | int | Count of fuiShape Elements in a file
| fuiShapeComponent Count | 0x5c | 4 | int | Count of fuiShapeComponent Elements in a file
| fuiVert Count | 0x60 | 4 | int | Count of fuiVert Elements in a file
| fuiTimelineFrame Count | 0x64 | 4 | int | Count of fuiTimelineFrame Elements in a file
| fuiTimelineEvent Count | 0x68 | 4 | int | Count of fuiTimelineEvent Elements in a file
| fuiReference Count | 0x6c | 4 | int | Count of fuiReference Elements in a file
| fuiEdittext Count | 0x70 | 4 | int | Count of fuiEdittext Elements in a file
| fuiSymbol Count | 0x74 | 4 | int | Count of fuiSymbol Elements in a file
| fuiBitmap Count | 0x78 | 4 | int | Count of fuiBitmap Elements in a file
| images size | 0x7c | 4 | int | Size of all Images in a file
| fuiFontName Count | 0x80 | 4 | int | Count of fuiFontName Elements in a file
| fuiImportAsset Count | 0x84 | 4 | int | Count of fuiImportAsset Elements in a file
| Frame Size | 0x88 | 0x10 | fuiRect | Size of the frame ?

## FUI Timeline
Timeline member:
| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Object Type | 0x0 | 4 | int | Type 2(fuiTimeline) of fuiObject.eFuiObjectType
| Unknown | 0x4 | 8 | short | 4 unknown short values
| Rectangle | 0xc | 0x10 | fuiRect | Unknown fuiRect

## fuiTimelineAction

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Unknown | 0x0 | 4 | short | 2 Unknown short values
| Unknown Name | 0x4 | 0x40 | char[] | Might be the Action name
| Unknown Name | 0x44 | 0x40 | char[] | Might be the argv for the action


## fuiShape

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Unknown Value | 0x0 | 4 | int | 
| Unknown Value | 0x4 | 4 | int | 
| Object Type | 0x8 | 4 | int | Type 1(fuiShape) of fuiObject.eFuiObjectType
| Rectangle | 0xc | 0x10 | fuiRect | Rectangle describing area of the shape points (maybe)

## fuiShapeComponent

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Fill Info | 0x0 | 0x24 | fuiFillStyle | Component Fill Info
| Unknown | 0x24 | 4 | int | 
| Unknown | 0x28 | 4 | int | 

## fuiVert

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| X | 0x0 | 4 | float | X Position of the Vertex
| Y | 0x4 | 4 | float | Y Position of the Vertex

## fuiTimelineFrame

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Frame Name | 0x0 | 0x40 | char[] | Name of the FUI Timeline Frame
| Unknown | 0x40 | 4 | int | 
| Unknown | 0x44 | 4 | int | 

## fuiTimelineEvent

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Unknown | 0x0 | 0xc | short | 6 unknown short values
| matrix | 0xc | 0x18 | fuiMatrix
| ColorTransform | 0x24 | 0x20 | fuiColorTransform |
| Color | 0x44 | 4 | fuiRGBA |

## fuiTimelineEventName

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Event Name | 0x0 | 0x40 | char[] | Name of the Timeline Event

## fuiReference

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Symbol Index | 0x0 | 4 | int | Index of Symbol (resolved at runtime)
| Reference Name | 0x4 | 0x40 | char[] | 
| Unknown | 0x44 | 4 | int | fuiFile Index (resolved at runtime)

## fuiEdittext

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Unknown | 0x0 | 4 | int | 
| rectangle | 0x4 | 0x10 | fuiRect | 
| Unknown | 0x14 | 4 | int | 
| Unknown | 0x18 | 4 | float | 
| Color | 0x1c | 4 | fuiRGBA | 
| Unknown | 0x20 | 0x18 | int | 6 unknwon int
| html text format | 0x38 | 0x100 | char[] | 

## fuiFontName

TODO: get proper names and types!

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Unknown | 0x0 | 4 | int | 
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
| Object Type | 0x40 | 4 | int | 
| Unknown | 0x44 | 4 | int | 

## fuiImportAsset

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Name | 0x0 | 0x40 | char[] | File Name to import from

## fuiBitmap

| Name | Offset | Byte Size | Type | Description |
| :-:|:-:|:-:|:-:|:-:|
| Unknown | 0x0 | 4 | int | Could be a kind of id
| Object Type | 0x4 | 4 | int | Type of the bitmap (1 = Shape, 3 = Bitmap) (not tested!)
| Scale Width | 0x8 | 4 | int | Width value to scale the given bitmap/Image data
| Scale Height | 0xc | 4 | int | Height value to scale the given bitmap/Image data
| Size 1 | 0x10 | 4 | int | Mostly used to identify compressed image size
| Size 2 | 0x14 | 4 | int | 
| Unknown | 0x18 | 4 | int | 
| Unknown | 0x1c | 4 | int | 
