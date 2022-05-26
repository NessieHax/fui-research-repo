from io import BufferedReader
from dataclasses import dataclass, field
from fuiDataStructures.fuiHeader import fuiHeader
from fuiDataStructures.fuiTimeline import fuiTimeline
from fuiDataStructures.fuiTimelineFrame import fuiTimelineFrame
from fuiDataStructures.fuiTimelineAction import fuiTimelineAction
from fuiDataStructures.fuiShape import fuiShape
from fuiDataStructures.fuiShapeComponent import fuiShapeComponent
from fuiDataStructures.fuiVert import fuiVert
from fuiDataStructures.fuiTimelineEvent import fuiTimelineEvent
from fuiDataStructures.fuiTimelineEventName import fuiTimelineEventName
from fuiDataStructures.fuiReference import fuiReference
from fuiDataStructures.fuiEdittext import fuiEdittext
from fuiDataStructures.fuiFontName import fuiFontName
from fuiDataStructures.fuiSymbol import fuiSymbol
from fuiDataStructures.fuiImportAsset import fuiImportAsset
from fuiDataStructures.fuiBitmap import fuiBitmap

@dataclass(slots=True)
class fuiFile:
    header: fuiHeader                                   = field(init=False)
    timelines: list[fuiTimeline]                        = field(default_factory=list, repr=False, init=False)
    timeline_actions: list[fuiTimelineAction]           = field(default_factory=list, repr=False, init=False)
    shapes: list[fuiShape]                              = field(default_factory=list, repr=False, init=False)
    shape_components: list[fuiShapeComponent]           = field(default_factory=list, repr=False, init=False)
    verts: list[fuiVert]                                = field(default_factory=list, repr=False, init=False)
    timeline_frames: list[fuiTimelineFrame]             = field(default_factory=list, repr=False, init=False)
    timeline_events: list[fuiTimelineEvent]             = field(default_factory=list, repr=False, init=False)
    timeline_event_names: list[fuiTimelineEventName]    = field(default_factory=list, repr=False, init=False)
    references: list[fuiReference]                      = field(default_factory=list, repr=False, init=False)
    edittexts: list[fuiEdittext]                        = field(default_factory=list, repr=False, init=False)
    font_names: list[fuiFontName]                       = field(default_factory=list, repr=False, init=False)
    symbols: list[fuiSymbol]                            = field(default_factory=list, repr=False, init=False)
    import_assets: list[fuiImportAsset]                 = field(default_factory=list, repr=False, init=False)
    bitmaps: list[fuiBitmap]                            = field(default_factory=list, repr=False, init=False)
    images: list[bytes]                                 = field(default_factory=list, repr=False, init=False)

    def parse(self, data: BufferedReader) -> None:
        self.header = fuiHeader(data.read(fuiHeader.size))
        def __make(container: list, cls, count: int, data: BufferedReader):
            [container.append(cls(data.read(cls.size))) for _ in range(count)]

        __make(self.timelines,              fuiTimeline,            self.header.timeline_count, data)
        __make(self.timeline_actions,       fuiTimelineAction,      self.header.timeline_action_count, data)
        __make(self.shapes,                 fuiShape,               self.header.shape_count, data)
        __make(self.shape_components,       fuiShapeComponent,      self.header.shape_component_count, data)
        __make(self.verts,                  fuiVert,                self.header.vert_count,     data)
        __make(self.timeline_frames,        fuiTimelineFrame,       self.header.timeline_frame_count, data)
        __make(self.timeline_events,        fuiTimelineEvent,       self.header.timeline_event_count, data)
        __make(self.timeline_event_names,   fuiTimelineEventName,   self.header.timeline_event_name_count, data)
        __make(self.references,             fuiReference,           self.header.reference_count, data)
        __make(self.edittexts,              fuiEdittext,            self.header.edittext_count, data)
        __make(self.font_names,             fuiFontName,            self.header.font_name_count, data)
        __make(self.symbols,                fuiSymbol,              self.header.symbol_count, data)
        __make(self.import_assets,          fuiImportAsset,         self.header.import_asset_count, data)
        __make(self.bitmaps,                fuiBitmap,              self.header.bitmap_count, data)
        for bitmap in self.bitmaps:
            self.images.append(data.read(bitmap.size))
                
