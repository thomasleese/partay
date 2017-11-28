# Partay 🎉

Helping you host a great PARTAY!

![](https://media.giphy.com/media/xUOxeY42XYR5tMUN7G/200w_d.gif)

By combining a number of different devices together with some software, it is
possible to host party with high production value very easily. At the moment,
the software works with iTunes, tvOS and Phillips Hue; but it could easily be
expanded in the future.

## Setup

The first thing to do is to install and run the
[tvOS replica application](tvos-replica) app on your Apple TV, and make sure
your Phillips Hue lights are all configured and working (note that this app
does not use HomeKit, instead uses the official API). Next, you can set up your
main device, i.e. the computer playing songs through iTunes. I would also
recommend using [Soundflower](https://github.com/mattingalls/Soundflower) to
loop your audio output back as input to avoid outside noise when controlling
the lights. Finally, you run the [primary application](primary) on that
machine, press play, and start the party.

## Features

- Any Phillips Hue lights will change in time to the music.
- Lyrics for the current song will be shown on your Apple TV.

## Detailed Instructions

1. Install [Xcode][xcode] and [Homebrew][homebrew] on your target computer.
2. Clone this repository to a location on your computer.
3. Run `pipenv install` to install the application.
4. Sign up for [Genius](https://genius.com) and get an API key.
5. [Get an API key for your Phillips Hue lights](https://developers.meethue.com/documentation/getting-started).
6. Run `pipenv run python -m partay config.yaml [<replica_address> ...]`

[xcode]: https://developer.apple.com/xcode/
[homebrew]: http://brew.sh
