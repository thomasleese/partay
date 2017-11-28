//
//  GameViewController.swift
//  Partay
//
//  Created by Thomas Leese on 20/12/2016.
//  Copyright © 2016 Thomas Leese. All rights reserved.
//

import UIKit
import SpriteKit
import Socket

class ViewController: UIViewController {

    @objc func server() {
        do {
            let socket = try Socket.create(family: .inet)

            try socket.listen(on: 1234)

            print("Listening on port: \(socket.listeningPort)")

            while true {
                let newSocket = try socket.acceptClientConnection()

                print("Accepted connection from: \(newSocket.remoteHostname) on port \(newSocket.remotePort)")

                do {
                    sleep(1)
                    let json = try newSocket.readString()!
                    if let song = Song.fromString(s: json) {
                        DispatchQueue.main.async {
                            self.songChanged(song)
                        }
                    } else {
                        print("Could not parse JSON!")
                        print(json)
                    }
                } catch {
                    print("Cannot read!")
                }

                newSocket.close()
            }
        } catch {
            print("Error")
        }
    }

    func songChanged(_ song: Song) {
        print("Song changed to: " + song.title)

        let transition = SKTransition.crossFade(withDuration: 2)

        let scene = SongScene(fileNamed: "SongScene")!
        scene.scaleMode = .aspectFill
        scene.loadSong(song)

        let view = self.view as! SKView
        view.presentScene(scene, transition: transition)
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        Thread(target: self, selector: #selector(ViewController.server), object: nil).start()

        if let view = self.view as! SKView? {
            let scene = WelcomeScene(fileNamed: "WelcomeScene")!
            scene.scaleMode = .aspectFill
                
            view.presentScene(scene)
            
            view.ignoresSiblingOrder = true
        }
    }

}
