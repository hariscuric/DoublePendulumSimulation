import graphics as gr
import time as t
import math as m



def computeAlpha1ddot(alpha1N,alpha2N,alpha1dotN,alpha2dotN,m1,m2,L1,L2):
    g=9.81
    term1 = -m1*g*m.sin(alpha1N)
    term2 = m2*(alpha2dotN**2)*L2*m.sin(alpha2N-alpha1N)
    term3 = m2*g*m.cos(alpha2N)*m.sin(alpha2N-alpha1N)
    term4 = m2*(alpha1dotN**2)*m.cos(alpha1N-alpha2N)*m.sin(alpha2N-alpha1N)
    term5 = m1*L1
    term6 = -m2*m.sin(alpha1N-alpha2N)*m.sin(alpha2N-alpha1N)*L1
    alpha1ddot = (term1+term2+term3+term4)/(term5 + term6)
    return alpha1ddot

def computeAlpha2ddot(alpha1N,alpha2N,alpha1dotN,L1,L2,alpha1ddot):
    g=9.81
    term1 = -g*m.sin(alpha2N)
    term2 = -alpha1ddot*L1*m.cos(alpha1N-alpha2N)
    term3 = (alpha1dotN**2)*L1*m.sin(alpha1N-alpha2N)
    term4 = L2
    alpha2ddot = (term1+term2+term3)/term4
    return alpha2ddot
    


def updateAlphas(alpha1N,alpha2N,alpha1dotN,alpha2dotN,timeStep,m1,m2,L1,L2):
    alpha1ddot = computeAlpha1ddot(alpha1N,alpha2N,alpha1dotN,alpha2dotN,m1,m2,L1,L2)

    alpha2ddot = computeAlpha2ddot(alpha1N,alpha2N,alpha1dotN,L1,L2,alpha1ddot)

    alpha1dotN = alpha1dotN + timeStep*alpha1ddot
    alpha1N = alpha1N + timeStep*alpha1dotN

    alpha2dotN = alpha2dotN + timeStep*alpha2ddot
    alpha2N = alpha2N + timeStep*alpha2dotN

    return alpha1N,alpha2N,alpha1dotN,alpha2dotN


def numericalIntergration(alpha1t0,alpha2t0,alpha1dott0,alpha2dott0,duration,timeStep,m1,m2,L1,L2):
    alpha1 = [alpha1t0]
    alpha2 = [alpha2t0]

    alpha1N,alpha2N,alpha1dotN,alpha2dotN = alpha1t0,alpha2t0,alpha1dott0,alpha2dott0

    for t in range(int(duration/timeStep)):
        alpha1N,alpha2N,alpha1dotN,alpha2dotN = updateAlphas(alpha1N,alpha2N,alpha1dotN,alpha2dotN,timeStep,m1,m2,L1,L2)
        alpha1.append(alpha1N)
        alpha2.append(alpha2N)
        
    return alpha1, alpha2




def inputData():
    Alpha1 = (m.pi/180)*float(input("Input initial angle (in degrees) of the top pendulum: "))
    Alpha2 = (m.pi/180)*float(input("Input initial angle (in degrees) of the bottom pendulum: "))
    Alpha1dot = (m.pi/180)*float(input("Input initial angle velocity (in degrees/s) of the top pendulum: "))
    Alpha2dot = (m.pi/180)*float(input("Input initial angle velocity (in degrees/s) of the bottom pendulum: "))
    m1 = float(input("Input the mass of the top pendulum (in kg): "))
    m2 = float(input("Input the mass of the bottom pendulum (in kg): "))
    L1 = float(input("Input the length of the top pendulum (in meters): "))
    L2 = float(input("Input the length of the bottom pendulum (in meters): "))
    duration = float(input("What is the duration of animation you want to produce (in seconds)?: "))


    return Alpha1,Alpha2,Alpha1dot,Alpha2dot,m1,m2,L1,L2,duration



def createAnimation(alpha1list,alpha2list,dt,duration,L1,L2):
    windowWidth = 700
    windowHeight = 700
    window = gr.GraphWin("Double Pendulum Motion", windowWidth, windowHeight)
    window.setBackground("black")
    window.setCoords(0,windowHeight,windowWidth,0)
    mainHingePt = gr.Point(int(windowWidth/2), int(windowHeight/2))
    mainHingeCir = gr.Circle(mainHingePt,10)
    mainHingeCir.setFill("red")
    mainHingeCir.draw(window)
    ratioL1 = L1/(L1+L2)
    ratioL2 = L2/(L1+L2)

    animationLenght = duration
    frameRate = 1/30
    numOfFrames = int(animationLenght/frameRate)
    AnimationAlpha1 = []
    AnimationAlpha2 = []

    for i in range(numOfFrames):
        AnimationAlpha1.append(alpha1list[int(i*frameRate/dt)])
        AnimationAlpha2.append(alpha2list[int(i*frameRate/dt)])



    for i in range(len(AnimationAlpha1)):
        Alpha1 = AnimationAlpha1[i]
        Alpha2 = AnimationAlpha2[i]
        

        Pt1x = windowWidth/2 + (windowHeight/3)*ratioL1*m.sin(Alpha1)
        Pt1y = windowHeight/2 + (windowHeight/3)*ratioL1*m.cos(Alpha1)
        Pt1 = gr.Point(int(Pt1x), int(Pt1y))
        Cir1 = gr.Circle(Pt1,5)
        Cir1.setFill("white")
        Cir1.draw(window)

        Pt2x = Pt1x + (windowHeight/3)*ratioL2*m.sin(Alpha2)
        Pt2y = Pt1y + (windowHeight/3)*ratioL2*m.cos(Alpha2)
        Pt2 = gr.Point(int(Pt2x), int(Pt2y))
        Cir2 = gr.Circle(Pt2,5)
        Cir2.setFill("white")
        Cir2.draw(window)

        Line1 = gr.Line(mainHingePt,Pt1)
        Line1.setOutline("white")
        Line1.draw(window)

        Line2 = gr.Line(Pt1,Pt2)
        Line2.setOutline("white")
        Line2.draw(window)
        t.sleep(frameRate)
        Line1.undraw()
        Cir1.undraw()
        Line2.undraw()
        Cir2.undraw()


    Text=gr.Text(gr.Point(int(windowWidth/2),int(windowHeight/10)),"ANIMATION FINISHED")
    Text.setOutline("white")
    Text.draw(window)

    Text1=gr.Text(gr.Point(int(windowWidth/2),int(2*windowHeight/10)),"Press Enter to repeat")
    Text1.setOutline("white")
    Text1.draw(window)

    Text2=gr.Text(gr.Point(int(windowWidth/2),int(3*windowHeight/10)),"Press ESC to exit")
    Text2.setOutline("white")
    Text2.draw(window)

    def keyPress():
            key = window.getKey()
            if key == "Return":
                window.close()
                createAnimation(alpha1list,alpha2list,dt,duration,L1,L2)
            elif key == "Escape":
                window.close()
            else: keyPress()


    keyPress()






def main():


    #Input the initial angles, angle velocities, masses and pendulum lengths and animation duration:
    Alpha1,Alpha2,Alpha1dot,Alpha2dot,m1,m2,L1,L2,duration=inputData()


    #Run the numerical integration method to compute the motion:
    dt=0.001
    alpha1list, alpha2list = numericalIntergration(Alpha1,Alpha2,Alpha1dot,Alpha2dot,duration+2,dt,m1,m2,L1,L2)


    #Animate the computed motion:
    createAnimation(alpha1list,alpha2list,dt,duration,L1,L2)






main()