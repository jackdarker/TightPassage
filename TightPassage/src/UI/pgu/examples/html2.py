"""<title>an example of html within gui</title>"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from src.UI.pgu.pgu import gui
from src.UI.pgu.pgu import html

app = gui.Desktop(width=780,height=800)

data = """
<h1>header 1</h1>
<h2 bgcolor='red'>header 2</h2>
<h3>header 3</h3>
<p>
	<font color="#990000">This text is hexcolor #990000</font><br />
	<font color="red">This text is red</font>
</p>
<textarea cols="50" rows="2">Text area!</textarea>
<pre>
	It's a thief in the night
		To come and grab you     
	
	It can creep up inside you 
		And consume you 
</pre>
<a href="http://www.tutorialehtml.com" target="_blank" title="HTML Tutorials">HTML Tutorials</a>
<div style='color: #88ffff;'>this is normal <b>this is bold</b> <i>this is italic</i> <u>this is underline</u></div>
"""
data2="""
<table border=1 bgcolor='yellow' width=200 align=center>
    <tr>
    <th bgcolor='#ffffee'>pgu
    <th bgcolor='red'>red
    <th bgcolor='green'>green
    <th bgcolor='blue'>blue
    
    <tr>
    <td bgcolor='white' border=1><img src='logo.gif'>
    <td border=1 style='padding:4px'>things:<br>apples,<br>fire trucks,<br>crabs,<br>and cherries
    <td border=1 style='padding:4px'>things: <ul>
        <li>grass
        <li>trees
        <li>snakes
        <li>scum
        </ul>
    <td border=1 style='padding:4px'>things: <ol>
        <li>water
        <li>sky
        <li>goats
        <li>pizza
        </ol>
</table>
    
<pre>    
class Desktop(App):
    def __init__(self,**params):
        params.setdefault('cls','desktop')
        App.__init__(self,**params)
</pre>

<div style='margin: 8px; padding: 8px; border: 1px; border-color: #88ffff; background: #eeffff;' width=700><img src='cuzco.png' align=right>cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. </div>"""

##this example just uses the HTML widget
##::
doc = html.HTML(data)
##

app.connect(gui.QUIT,app.quit,None)
app.run(doc)
