from util.gui_helper import show_message


# Part of animation taken proudly from here:
# https://codegolf.stackexchange.com/questions/24462/display-the-explosion-of-a-star-in-ascii-art
def do_super_important_things():
    animation = [
        r'''
    
    
    
                                __------__
                              /~          ~\
                             |    //^\\//^\|
                           /~~\  ||  o| |o|:~\
                          | |9   ||___|_|_||:|
                           \__.  /      o  \/'
                            |   (       O   )
                   /~~~~\    `\  \         /
                  | |~~\ |     )  ~------~`\
                 /' |  | |   /     ____ /~~~)\
                (_/'   | | |     /'    |    ( |
                       | | |     \    /   __)/ \
                       \  \ \      \/    /' \   `\
                         \  \|\        /   | |\___|
                           \ |  \____/     | |
                           /^~>  \        _/ <
                          |  |         \       \
                          |  | \        \        \
                          -^-\  \       |        )
                               `\_______/^\______/

        ''',
        r'''



                                __------__
                              /~          ~\
                             |    //^\\//^\|
                           /~~\  ||  -| |-|:~\
                          | |8   ||___|_|_||:|
                           \__.  /      o  \/'
                            |   (       O   )
                   /~~~~\    `\  \         /
                  | |~~\ |     )  ~------~`\
                 /' |  | |   /     ____ /~~~)\
                (_/'   | | |     /'    |    ( |
                       | | |     \    /   __)/ \
                       \  \ \      \/    /' \   `\
                         \  \|\        /   | |\___|
                           \ |  \____/     | |
                           /^~>  \        _/ <
                          |  |         \       \
                          |  | \        \        \
                          -^-\  \       |        )
                               `\_______/^\______/

        ''',
        r'''



                                __------__
                              /~          ~\
                             |    //^\\//^\|
                           /~~\  ||  0| |0|:~\
                          | |7   ||___|_|_||:|
                           \__.  /      o  \/'
                            |   (       O   )
                   /~~~~\    `\  \         /
                  | |~~\ |     )  ~------~`\
                 /' |  | |   /     ____ /~~~)\
                (_/'   | | |     /'    |    ( |
                       | | |     \    /   __)/ \
                       \  \ \      \/    /' \   `\
                         \  \|\        /   | |\___|
                           \ |  \____/     | |
                           /^~>  \        _/ <
                          |  |         \       \
                          |  | \        \        \
                          -^-\  \       |        )
                               `\_______/^\______/

        ''',
        r'''



                                __------__
                              /~          ~\
                             |    //^\\//^\|
                           /~~\  ||  o| |o|:~\
                          | |6   ||___|_|_||:|
                           \__.  /      o  \/'
                            |   (       O   )
                   /~~~~\    `\  \         /
                  | |~~\ |     )  ~------~`\
                 /' |  | |   /     ____ /~~~)\
                (_/'   | | |     /'    |    ( |
                       | | |     \    /   __)/ \
                       \  \ \      \/    /' \   `\
                         \  \|\        /   | |\___|
                           \ |  \____/     | |
                           /^~>  \        _/ <
                          |  |         \       \
                          |  | \        \        \
                          -^-\  \       |        )
                               `\_______/^\______/

        ''',
        r'''



                                __------__
                              /~          ~\
                             |    //^\\//^\|
                           /~~\  ||  -| |-|:~\
                          | |5   ||___|_|_||:|
                           \__.  /      o  \/'
                            |   (       O   )
                   /~~~~\    `\  \         /
                  | |~~\ |     )  ~------~`\
                 /' |  | |   /     ____ /~~~)\
                (_/'   | | |     /'    |    ( |
                       | | |     \    /   __)/ \
                       \  \ \      \/    /' \   `\
                         \  \|\        /   | |\___|
                           \ |  \____/     | |
                           /^~>  \        _/ <
                          |  |         \       \
                          |  | \        \        \
                          -^-\  \       |        )
                               `\_______/^\______/

        ''',
        r'''



                                __------__
                              /~          ~\
                             |    //^\\//^\|
                           /~~\  ||  o| |o|:~\
                          | |4   ||___|_|_||:|
                           \__.  /      o  \/'
                            |   (       O   )
                   /~~~~\    `\  \         /
                  | |~~\ |     )  ~------~`\
                 /' |  | |   /     ____ /~~~)\
                (_/'   | | |     /'    |    ( |
                       | | |     \    /   __)/ \
                       \  \ \      \/    /' \   `\
                         \  \|\        /   | |\___|
                           \ |  \____/     | |
                           /^~>  \        _/ <
                          |  |         \       \
                          |  | \        \        \
                          -^-\  \       |        )
                               `\_______/^\______/

        ''',
        r'''


                 
                                __------__
                              /~          ~\
                             |    //^\\//^\|
                           /~~\  ||  -| |-|:~\
                          | |3   ||___|_|_||:|
                           \__.  /      o  \/'
                            |   (       O   )
                   /~~~~\    `\  \         /
                  | |~~\ |     )  ~------~`\
                 /' |  | |   /     ____ /~~~)\
                (_/'   | | |     /'    |    ( |
                       | | |     \    /   __)/ \
                       \  \ \      \/    /' \   `\
                         \  \|\        /   | |\___|
                           \ |  \____/     | |
                           /^~>  \        _/ <
                          |  |         \       \
                          |  | \        \        \
                          -^-\  \       |        )
                               `\_______/^\______/

        ''',
        r'''



                                __------__
                              /~          ~\
                             |    //^\\//^\|
                           /~~\  ||  -| |-|:~\
                          | |2   ||___|_|_||:|
                           \__.  /      o  \/'
                            |   (       O   )
                   /~~~~\    `\  \         /
                  | |~~\ |     )  ~------~`\
                 /' |  | |   /     ____ /~~~)\
                (_/'   | | |     /'    |    ( |
                       | | |     \    /   __)/ \
                       \  \ \      \/    /' \   `\
                         \  \|\        /   | |\___|
                           \ |  \____/     | |
                           /^~>  \        _/ <
                          |  |         \       \
                          |  | \        \        \
                          -^-\  \       |        )
                               `\_______/^\______/

        ''',
        r'''
        
        

                                __------__
                              /~          ~\
                             |    //^\\//^\|
                           /~~\  ||  -| |-|:~\
                          | |1   ||___|_|_||:|
                           \__.  /      o  \/'
                            |   (       O   )
                   /~~~~\    `\  \         /
                  | |~~\ |     )  ~------~`\
                 /' |  | |   /     ____ /~~~)\
                (_/'   | | |     /'    |    ( |
                       | | |     \    /   __)/ \
                       \  \ \      \/    /' \   `\
                         \  \|\        /   | |\___|
                           \ |  \____/     | |
                           /^~>  \        _/ <
                          |  |         \       \
                          |  | \        \        \
                          -^-\  \       |        )
                               `\_______/^\______/

        ''',
        r'''






                                 @@@@@@@@@@@@@@@
                               @@@@@@@@@@@@@@@@@@@
                             @@@@@@@@@@@@@@@@@@@@@@@
                            @@@@@@@@@@@@@@@@@@@@@@@@@
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@
                           @@@@@@@@@@@oooo@@@@@@@@@@@@
                           @@@@@@@@@@@ooo@@@@@@@@@@@@@
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@
                            @@@@@@@@@@@@@@@@@@@@@@@@@
                             @@@@@@@@@@@@@@@@@@@@@@@
                               @@@@@@@@@@@@@@@@@@@
                                 @@@@@@@@@@@@@@@





        ''',
        r'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%oooo % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  oooooo% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ooooo   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    o  % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ''',
        r'''
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHH HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH HHHHHHHHHHHHHHH HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH HHHHHHH HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH HHHHHH HHHHHHH HHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH.HHHHH HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH. HH   HH H HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHH HHH   o ooooo : HHH .HHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH .oooooooooo   .. HHHHHHHHH HHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHH  HHHH  ooooooooooooo:  HHH H HHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHH ...oooooooooooooo  . . HHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHH  oooooooooooooo.ooo  HH HHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHH HHHHH .H H:.ooooooooooooo!o!:.: :HH.HHH  H HHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHH ooooooooooooooo:  . HHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHH H. ..oooo!oo:ooo.  ..: HHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHH .  HHH   !.o::.ooo.o. .  HHH H.HHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHH HHHHHHHHH HH   H  . .  :  H :.HHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHH HHHHHHHHHHH H HH  :   .   H   H .HHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHH H HHHHH.HHH HHH HH HHHH HHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH HHHHH HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        ''',
        r'''
  :@o WoOo@oo@ooo%o@ooo$0%&oo@ @=O&o&oO+ooooo&oOo+-o+0@&%0o@@@&-$&=&o%MHo# $:.
oo.#o :&o$@Mo$@&o=-oooo&%o#@Ooo o=O&&=+ oo+--o@O   O8==o&0000O-%OO&$%%M#  H$ .::
&o@MooO&ooW&Hoo$oooo+oOo0ooo0=+ o=+=+-o  o+-8=o-+  @0&$=88+@+0 &@&$#000O@!%HOMW#
M0@#%#%#%W$oHoooo&oo O@oo=O00o++o+-@ 8-o  -Oo-   ++00-O=+o  O=0&8@#&H$#$W#%%$MOO
ooo-@ooo@ooo#@%&Oooo8o+oo-++OoOo- - -+-   -     -+++@++= -+oO@#o80W0@$&&0@8WO#IO
#8=oW oo&o@oO8o0@O@&oO++o  -  O-     =    -   @  -=+- - ++8o%8$$@&0@=0&%#-+M W$@
oWW@o0@%ooo 0o@8+88O8@8+8o-  - +=o            o +o   + -=08@oOOOO0 =+@=+ 0800%$#
!$MOO#ooo&o@@o0@-0   o=O- --          @      @  o     - O+++-@ O--8@O@@8@$%WMI#!
o!#I%@$I#W&%o08=O -=O= o-o =   o             o     @      @ --=8+=80&$$0@M!!%$HI
@MHo!@I@oo%$o%0@&00o+o-@  o                      o         -+O=@==0888MWH0I&IH%
Wooo$@&o#o8o@oo&==o8O 8---o               o@             + @8=+$00@&%$#@&$##$#%#
oOoWoo%88O0Ooo+ooo++o@  -o@   @                         - --+++=OO====0@@8@&@#&@
o8+&o%0 o0O@+=  o +o                                   @    -o  =++O@O - -$=MO=%
$&&OoOo8O0o@Oo=ooo+++-- -@  -                       @    --++++==OOO0@=OO@&=@O@#
@###%%o#&@ooo&&o&+-oooo@+-   @o              @o       @--@8+ 00=O%$%0$%%%$$WW%#W
@MI&oI@#!MOOoW%$088O+-  -                .           o     ++=O=0&%@W$#WII0!.I&!
ooIW#WoMo$@&o0o8oo 8o@+o-  o @  o  o  @             +     -- 8 =+O80@0#0IW@I !I
o:$@#o@ooo$=--@@oo8o +o8o@+@    o      @          o  -o 8+@o-Oo8o8==O80@@$$%#%II
@WW#%Wo==+ooOo -OOOo8o@o@---          -  @       -     --Oo@@88O==+0 0&@&@8%$$@#
oO0#-$= @&-8@80o&O=80@+@-=@ -+-      @    o    o +o -   -+O+oO0O$@00OO+=@M+0&8@O
=H%$##0o@$$o%%&O&W$&O=-  -+++8=-   @+-     -+  -  +-8+-O- OO8O&@%OW%@$&%@&08-&++
+0&M@##W$@O&$W0$$&@88@=+-=8-8O+-   = +--  -+ --   +=-===+=80Oo0$0&@@@M#%M#%#M%0&
WWMWOIHO!WO!:$%@@@O+ 8ooO&8&==+  -+=+0+  -+O@-+- o+=8&8O8=@= &@0@$&$#I:&M%!O#MWW
I!O#I#o I&%O$$&%80 8Ooo0#@$8O=  ===$00+ -++8@=@== 8OO&=0%@0@+8 =0&@$#$%W& :O#I.!
        ''',
        r'''
  8 ooo o    oo ooo     o o  o        o  o    o        @         o         oO+&@
  o-  =   o      o       o                                          o   -    -
       - -
                  oo                                 o
                              .                 o   
  o           o                                 
o               o                                  o
o       o           o                          .
 O          o                                    @                            ++
 o-   o             o                              .
 o  o                o
 oo    oo  o        o
         o
   o                                                                  o
  o  oo
+          oo o o          .                                                  -
   o                                                      o
               o      o       o
                                 .
o  o   o         . o         .                             o            o
o    @        o                                       o             o
  o             o                                                o  o
        o                                  o      .   o               -+ -
  -=  8-                                                                   8O  
        ''',
        r'''


.
    .



          .





                                                                                







 o


        ''',
        r'''
























        ''',
    ]
    for _ in range(300):
        animation.append(animation[-1])
    show_message('!!! Error: Mind = Blown !!!', animation, toggle_interval=0.2)
