//
//  Song.swift
//  Partay
//
//  Created by Thomas Leese on 20/12/2016.
//  Copyright © 2016 Thomas Leese. All rights reserved.
//

import Foundation

struct Song {

    var title: String
    var artist: String
    var album: String
    var duration: Int
    var lyrics: String?

    static func fromString(s: String) -> Song? {
        let data = s.data(using: .utf8)!
        var json: [String: AnyObject?]!
        do {
            json = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [String: AnyObject?]
        } catch {
            return nil
        }

        let song = Song(title: json["title"] as! String, artist: json["artist"] as! String, album: json["album"] as! String, duration: json["duration"] as! Int, lyrics: json["lyrics"] as! String?)
        return song
    }

}
