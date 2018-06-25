let drivecode = 0
let y = 0
let x = 0
function DriveBot()  {
   x = input.acceleration(Dimension.X)
   y = input.acceleration(Dimension.Y)
   drivecode = (y / 8 + 128) * 256 + (x / 8 + 128)
   radio.sendNumber(drivecode)
   if (y < -512) {
       if (x < -512) {
           basic.showLeds(`
               # # # . .
               # # . . .
               # . # . .
               . . . # .
               . . . . .
               `)
       } else {
           if (x > 512) {
               basic.showLeds(`
                   . . # # #
                   . . . # #
                   . . # . #
                   . # . . .
                   . . . . .
                   `)
           } else {
               basic.showLeds(`
                   . . # . .
                   . # # # .
                   # . # . #
                   . . # . .
                   . . # . .
                   `)
           }
       }
   } else {
       if (y > 512) {
           if (x < -512) {
               basic.showLeds(`
                   . . . . .
                   . . . # .
                   # . # . .
                   # # . . .
                   # # # . .
                   `)
           } else {
               if (x > 512) {
                   basic.showLeds(`
                       . . . . .
                       . # . . .
                       . . # . #
                       . . . # #
                       . . # # #
                       `)
               } else {
                   basic.showLeds(`
                       . . # . .
                       . . # . .
                       # . # . #
                       . # # # .
                       . . # . .
                       `)
               }
           }
       } else {
           if (x < -512) {
               basic.showLeds(`
                   . . # . .
                   . # . . .
                   # # # # #
                   . # . . .
                   . . # . .
                   `)
           } else {
               if (x > 512) {
                   basic.showLeds(`
                       . . # . .
                       . . . # .
                       # # # # #
                       . . . # .
                       . . # . .
                       `)
               } else {
                   if (x < -128 || x > 128 || (y < -128 || y > 128)) {
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
radio.setGroup(4)
basic.showNumber(4)
basic.forever(() => {
   if (input.buttonIsPressed(Button.A)) {
       DriveBot()
   } else {
       radio.sendNumber(0)
       basic.showLeds(`
           . # # # .
           # . . # #
           # . # . #
           # # . . #
           . # # # .
           `)
   }
   basic.pause(100)
})
