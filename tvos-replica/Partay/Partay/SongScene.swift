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
        let margin = 60
        let gap = 30

        if let lyrics = song.lyrics {
            let lines = lyrics.components(separatedBy: .newlines)
            let totalHeight = margin + margin + lines.count * gap

            var y = -margin
            for line in lyrics.components(separatedBy: .newlines) {
                y -= gap
                createLine(line, y, y + totalHeight, Float(song.duration) / 1000.0)
            }


        }

    }

    func createLine(_ line: String, _ y: Int, _ targetY: Int, _ duration: Float) {
        let node = SKLabelNode(text: line)
        node.position = CGPoint(x: 0, y: y)
        node.fontSize = 18
        addChild(node)

        let moveNodeUp = SKAction.moveBy(x: 0.0,
                                         y: CGFloat(targetY),
                                         duration: TimeInterval(duration))
        node.run(moveNodeUp)
    }

}
