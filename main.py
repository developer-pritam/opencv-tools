import argparse
import sys
import os
from rich.console import Console
from pyfiglet import Figlet
import src.VolumeControllerUtil as vc
import src.BrightnessControllerUtil as bc
import src.QRCodeUtil as qr
import src.MouseControllerUtil as mc

name = "Pritam"

pc = Console()

def Commands():
    pc.print("Basic terminal commands : ", style='cyan')
    pc.print("ls : ", style='pink1', end='')
    pc.print("Displaying all Commands ", ":search:", style='bright_white')
    pc.print("exit : ", style='orange_red1', end='')
    pc.print("For Exit from "+name, style='bright_white')
    pc.print("clear : ", style='orchid2', end='')
    pc.print("Clear your Screen", style='bright_white')
    pc.print('back : ', style='purple', end='')
    pc.print('Back to Main Menu', style='yellow')
    pc.print('main : ', style='purple', end='')
    pc.print('Go to Main Menu', style='yellow')  
    return " "  

def clear():
    # for windows screen
    if sys.platform.startswith('win'):
        os.system('cls')
    # for mac or linux          
    else:
        os.system('clear')
                
def banner():
    clear()
    banner = Figlet(font='isometric3',justify='right')
    pc.print(banner.renderText(name),style="bold red")
    pc.print("                         Python Open-CV and MediaPipe Project                                                                                              ", style="cyan1")
    print(" ")
    print(" ")
    pc.print("                         @Pritam, @Pranav and @Pankaj                         " , style='bold red')                                                   

def _out():
    pc.print("Thank you for using "+ name +"!", style="yellow")
    sys.exit(0)


parser = argparse.ArgumentParser(description="Recon with "+ name + Commands())
args = parser.parse_args()


def main():
    banner()    
    pc.print("  \n> 1 for Volume Control ",style="bright_yellow")
    pc.print("  \n> 2 for Brightness Control ",style="green3")
    pc.print("  \n> 3 for Guesture Mouse ",style="red")
    pc.print("  \n> 4 for Barcode/QR code Scanner ",style="blue")
    pc.print("  \n> 5 for Exit ")
    print(" ")
    pc.print("> Choose one option : ",style='purple',end='')
    u_input = str(input())
    
    try:

        if u_input == '1':
        
            pc.print("  \n> Press 'q' for exiting/quitting",style="bright_yellow")
            print(" ")
            vc.start()
                                                                                                                           
            commands = {
            'ls': Commands,
            'help': Commands,
            'clear': clear,
            'quit': quit,
            'exit': _out,
            'back' : main,
            'main' : main
            }

            while True:
                print(" ")
                pc.print("~/"+ name+ " Command >$ ", style='purple', end='')
                user_input = input()                
                cmd = commands.get(user_input)
                if cmd:
                    cmd()                    
                elif user_input == '':
                    print("") 
                else:
                    pc.print("ILLEGAL COMMAND", style="red")                  
             
        if u_input == '2':
            pc.print("  \n> Press 'q' for exiting/quiting",style="bright_yellow")
            print(" ")
            bc.start()
                                                                                                                      
            commands = {
            'ls': Commands,
            'help': Commands,
            'clear': clear,
            'quit': quit,
            'exit': _out,
            'back' : main,
            'main' : main
            }

            while True:
                pc.print("~/" +name+ " Command >$ ", style='purple', end='')
                user_input = input()
                cmd = commands.get(user_input)
                if cmd:
                    cmd()        
                elif user_input == '':
                    print("")
                else:
                    pc.print("ILLEGAL COMMAND", style="red")
        
        if u_input == '3':
            pc.print("  \n> Press 'q' for exiting/quiting",style="bright_yellow")
            print(" ")
            mc.start()
                                                                                                                      
            commands = {
            'ls': Commands,
            'help': Commands,
            'clear': clear,
            'quit': quit,
            'exit': _out,
            'back' : main,
            'main' : main
            }

            while True:
                pc.print("~/" +name+ " Command >$ ", style='purple', end='')
                user_input = input()
                cmd = commands.get(user_input)
                if cmd:
                    cmd()        
                elif user_input == '':
                    print("")
                else:
                    pc.print("ILLEGAL COMMAND", style="red")
                
        if u_input == '4':
            pc.print("  \n> Press 'q' for exiting/quiting",style="bright_yellow")
            print(" ")
            qr.start()
                                                                                                                      
            commands = {
            'ls': Commands,
            'help': Commands,
            'clear': clear,
            'quit': quit,
            'exit': _out,
            'back' : main,
            'main' : main
            }

            while True:
                pc.print("~/" +name+ " Command >$ ", style='purple', end='')
                user_input = input()
                cmd = commands.get(user_input)
                if cmd:
                    cmd()        
                elif user_input == '':
                    print("")
                else:
                    pc.print("ILLEGAL COMMAND", style="red")

        if u_input == '5':
            sys.exit(0)
        
        if u_input == 'exit':
            sys.exit(0)

        if KeyboardInterrupt:
            pc.print('Invalid Option! Try Again.... ', style='bold red')
            pc.print('Do you want to choose again ? (y/n)', style='red')
            io = input()
            if io == 'y' or 'Y':
                main()
            elif io == 'n' or 'N':
                sys.exit(0)
            else:
                print('Not a option! Good Bye!')
                sys.exit(0)
        
        else:
            pc.print('Invalid Option! ',style='bright_red')
            sys.exit(0)
          
    except Exception as e:
        pc.print(e,style='orange1')        

    


if __name__ == '__main__':
    main()    
