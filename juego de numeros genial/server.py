from flask import Flask, render_template, request, redirect, session
from datetime import date
import random

app = Flask(__name__)
app.secret_key = 'session_counter_rafael'

#variable para los ganadores no importa si se limpia la sesion
ganadores = []

#ruta principal
@app.route('/')
def adivinar_numero():

  if 'intentos' not in  session: session['intentos'] = 0
  if 'mayor' not in session: session['mayor'] = False
  if 'ganador' not in session: session['ganador'] = False
  session['ganadores'] = []

  if 'numero_adivinar' not in session: session['numero_adivinar'] = random.randint(1,100)

  print(f"cheat del juego: el numero a adivinar es {session['numero_adivinar']}",flush=True)

  return render_template('main.html')


#demo de procesar para que tenga multiples comportamientos con una sola pagina hmtl
#si redireccionar a otras rutas ni renderizar a otras paginas
@app.route('/procesar', methods=['POST'])
def validar_numero():
  #se declara como global para poder modificar los valores de la variable global
  global ganadores

  #se inicializan varibles
  ganador = ''
  numero_introducido = 0
  mayormenor = ["Menor","Mayor"]

  #si se dio clic el boton de otra partida si gano o perdio
  if request.form['otrapartida']  == 'True':
    print('se presiono el boton otra partida')
    # si gano y mando el input no vacio se registra en la lista de ganadores
    if 'ganador' in session:
      print('el valor de session ganador es ' + str(session['ganador']))
      if session['ganador']:
        ganador = request.form['nombre_ganador'].strip()
        if ganador != '':
          print('el valor del nombre del ganador ' + request.form['nombre_ganador'].strip())
          ganadores.append({'ganador':ganador,'intentos':session['intentos'],'fecha':str(date.today())})
          print('lista de ganadores : ',end='\n')
          print(ganadores)
    #se reseta la sesion para iniciar otro juego
    session.clear()
  #de lo contrario entonces se le dio al boton de probar aun no ha ganado ni perdido
  else:
    #el numero introducido es si se presiono el boton procesar
    
    if request.form['numero_introducido'].strip() == '': 
      numero_introducido = 0
    else:  
      numero_introducido = int(request.form['numero_introducido'])

    #si el numero introducido es igual al numero a adivinar gano el usuario!
    if numero_introducido == session['numero_adivinar'] and numero_introducido !=0:
      session['ganador']=True
    #de lo contrario se cuentan los intentos
    else:
      session['intentos']+=1

    #si intentos es menor que 5 todavia tiene oportunidad
    if session['intentos'] < 5:
      #se deterina si el numero es mayor o menor al que se esta adivinando
      session['mayor'] = True if numero_introducido < session['numero_adivinar'] else False
      print("fallaste intenta de nuevo, el numero es " + str(session['intentos']) + f"te quedan {mayormenor[session['mayor']]} intentos",flush=True)
    #si intentos es igual a 5 perdio el usuario
    else:
      print("perdiste",flush=True)


  return redirect('/')

#se muestra la tabla de ganadores
@app.route('/mostrarganadores')
def mostrarganadores():
  session['ganadores'] = ganadores
  print('la variable de sesion ganadores vale : ',end='\n')
  print(session['ganadores'])
  return render_template('/ganadores.html')

#se cancela el juego y se limpia la session
@app.route('/resetearjuego')
def mcancelarjuego():
  session.clear()
  return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
