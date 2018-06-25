let Drive = 0
let decodeX = 0
let y = 0
let decodeY = 0
let power = 0
let Turn = 0
let x = 0
let stoptimer = 0
input.onButtonPressed(Button.B, () => {
   Stop()
})
function Forwards()  {
   pins.analogWritePin(AnalogPin.P8, power)
   pins.digitalWritePin(DigitalPin.P12, 0)
   pins.analogWritePin(AnalogPin.P0, power)
   pins.digitalWritePin(DigitalPin.P16, 0)
}
function FwdLeft()  {
   pins.analogWritePin(AnalogPin.P8, power)
   pins.digitalWritePin(DigitalPin.P12, 0)
   pins.digitalWritePin(DigitalPin.P0, 0)
   pins.digitalWritePin(DigitalPin.P16, 0)
}
function Backwards()  {
   pins.digitalWritePin(DigitalPin.P8, 0)
   pins.analogWritePin(AnalogPin.P12, power)
   pins.digitalWritePin(DigitalPin.P0, 0)
   pins.analogWritePin(AnalogPin.P16, power)
}
radio.onDataPacketReceived( ({ receivedNumber }) =>  {
   stoptimer = 0
   decodeY = receivedNumber / 256
   decodeX = receivedNumber - decodeY * 256
   Turn = decodeX - 128
   Drive = 128 - decodeY
   if (receivedNumber != 0) {
       if (input.buttonIsPressed(Button.B)) {
           basic.showString("D" + Drive)
           basic.showString("T" + Turn)
       } else {
           displayDriveValues()
       }
   } else {
       basic.showLeds(`
           . # # # .
           # . . # #
           # . # . #
           # # . . #
           . # # # .
           `)
       Coast()
   }
})
function displayDriveValues()  {
   x = Turn * 8
   y = 0 - Drive * 8
   Drive = Drive * 4
   Turn = Turn * 4
   power = Drive
   if (y < -128) {
       if (x < -128) {
           basic.showLeds(`
               # # # . .
               # # . . .
               # . # . .
               . . . # .
               . . . . .
               `)
           FwdLeft()
       } else {
           if (x > 128) {
               basic.showLeds(`
                   . . # # #
                   . . . # #
                   . . # . #
                   . # . . .
                   . . . . .
                   `)
               FwdRight()
           } else {
               basic.showLeds(`
                   . . # . .
                   . # # # .
                   # . # . #
                   . . # . .
                   . . # . .
                   `)
               Forwards()
           }
       }
   } else {
       if (y > 128) {
           power = 0 - Drive
           if (x < -128) {
               basic.showLeds(`
                   . . . . .
                   . . . # .
                   # . # . .
                   # # . . .
                   # # # . .
                   `)
               BwdLeft()
           } else {
               if (x > 128) {
                   basic.showLeds(`
                       . . . . .
                       . # . . .
                       . . # . #
                       . . . # #
                       . . # # #
                       `)
                   BwdRight()
               } else {
                   basic.showLeds(`
                       . . # . .
                       . . # . .
                       # . # . #
                       . # # # .
                       . . # . .
                       `)
                   Backwards()
               }
           }
       } else {
           if (x < -128) {
               basic.showLeds(`
                   . . # . .
                   . # . . .
                   # # # # #
                   . # . . .
                   . . # . .
                   `)
               power = 0 - Turn
               TurnLeft()
           } else {
               if (x > 128) {
                   basic.showLeds(`
                       . . # . .
                       . . . # .
                       # # # # #
                       . . . # .
                       . . # . .
                       `)
                   power = Turn
                   TurnRight()
               } else {
                   Coast()
                   if (x < -64 || x > 64 || (y < -64 || y > 64)) {
                       basic.showLeds(`
                           . . . . .
                           . . # . .
                           . # # # .
                           . . # . .
                           . . . . .
                           `)
                   } else {
                       basic.showLeds(`
                           . . . . .
                           . . . . .
                           . . # . .
                           . . . . .
                           . . . . .
                           `)
                   }
               }
           }
       }
   }
}
function TurnRight()  {
   pins.analogWritePin(AnalogPin.P8, power)
   pins.digitalWritePin(DigitalPin.P12, 0)
   pins.digitalWritePin(DigitalPin.P0, 0)
   pins.analogWritePin(AnalogPin.P16, power)
}
function TurnLeft()  {
   pins.digitalWritePin(DigitalPin.P8, 0)
   pins.analogWritePin(AnalogPin.P12, power)
   pins.analogWritePin(AnalogPin.P0, power)
   pins.digitalWritePin(DigitalPin.P16, 0)
}
function Stop()  {
   pins.digitalWritePin(DigitalPin.P8, 1)
   pins.digitalWritePin(DigitalPin.P12, 1)
   pins.digitalWritePin(DigitalPin.P0, 1)
   pins.digitalWritePin(DigitalPin.P16, 1)
}
function BwdLeft()  {
   pins.digitalWritePin(DigitalPin.P8, 0)
   pins.analogWritePin(AnalogPin.P12, power)
   pins.digitalWritePin(DigitalPin.P0, 0)
   pins.digitalWritePin(DigitalPin.P16, 0)
}
function Coast()  {
   pins.digitalWritePin(DigitalPin.P8, 0)
   pins.digitalWritePin(DigitalPin.P12, 0)
   pins.digitalWritePin(DigitalPin.P0, 0)
   pins.digitalWritePin(DigitalPin.P16, 0)
}
function BwdRight()  {
   pins.digitalWritePin(DigitalPin.P8, 0)
   pins.digitalWritePin(DigitalPin.P12, 0)
   pins.digitalWritePin(DigitalPin.P0, 0)
   pins.analogWritePin(AnalogPin.P16, power)
}
function FwdRight()  {
   pins.digitalWritePin(DigitalPin.P8, 0)
   pins.digitalWritePin(DigitalPin.P12, 0)
   pins.analogWritePin(AnalogPin.P0, power)
   pins.digitalWritePin(DigitalPin.P16, 0)
}
Turn = 0
radio.setGroup(4)
stoptimer = 0
power = 0
basic.showNumber(4)
basic.forever(() => {
   if (stoptimer > 10) {
       basic.showLeds(`
           # . . . #
           . # . # .
           . . # . .
           . # . # .
           # . . . #
           `)
       Stop()
       stoptimer = 0
   } else {
       stoptimer += 1
       basic.pause(100)
   }
})
