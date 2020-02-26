from pynput import keyboard

def on_press(key):
    try:
        print ('key {0} pressed'.format(key.char))
    except ArithmeticError:
        print ('speical key {0} pressed'.format(key))


def on_release(key):
    print ('{0} released'.format(key))
    if key==keyboard.Key.esc:
        #stop listener
        return False

#collect events until released
with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()

#....or,in a non-blocking fashion:
listener=keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
