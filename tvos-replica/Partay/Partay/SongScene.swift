//
//  SongScene.swift
//  Partay
//
//  Created by Thomas Leese on 20/12/2016.
//  Copyright © 2016 Thomas Leese. All rights reserved.
//

import SpriteKit

class SongScene: SKScene {

    func loadSong(_ song: Song) {
        let gap = 96
        let duration = Float(song.duration) / 1000.0 - 1 // song started

        if let lyrics = song.lyrics {
            let lines = lyrics.components(separatedBy: .newlines)
            let totalHeight = lines.count * gap + 500

            var y = -250
            for line in lyrics.components(separatedBy: .newlines) {
                y -= gap
                createLine(line, y, totalHeight, duration)
            }


        }

    }

    func createLine(_ line: String, _ y: Int, _ targetY: Int, _ duration: Float) {
        let node = SKLabelNode(text: line)
        node.position = CGPoint(x: 0, y: y)
        node.fontSize = 72
        node.fontName = "Helvetica Neue Thin"
        addChild(node)

        let moveNodeUp = SKAction.moveBy(x: 0.0,
                                         y: CGFloat(targetY),
                                         duration: TimeInterval(duration))
        node.run(moveNodeUp)
    }

}
