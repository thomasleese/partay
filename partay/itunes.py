"""iTunes related classes and functions."""

from collections import namedtuple

import Foundation
from AppKit import *
import objc
from PyObjCTools import AppHelper


Song = namedtuple('Song', ['title', 'artist', 'album', 'duration'])


class GetSongsObserver(NSObject):
    """An observer which handles song changes from iTunes."""

    def initWithCallback_(self, callback):
        self = objc.super(GetSongsObserver, self).init()
        if self is None:
            return None

        self.callback = callback
        return self

    def getMySongs_(self, song):
        user_info = song.userInfo()
        details = dict(user_info)

        if details['Player State'] == 'Playing':
            song  = Song(details['Name'], details['Artist'], details['Album'],
                         details['Total Time'])
            self.callback(song)


def listen(callback):
    """Listen for song changes and trigger the callback for each."""

    nc = Foundation.NSDistributedNotificationCenter.defaultCenter()
    observer = GetSongsObserver.alloc().initWithCallback_(callback)
    nc.addObserver_selector_name_object_(observer, 'getMySongs:',
                                         'com.apple.iTunes.playerInfo', None)

    AppHelper.runConsoleEventLoop()


if __name__ == '__main__':
    listen(lambda song: print(song))
