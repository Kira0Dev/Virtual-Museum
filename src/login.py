#login.py
from usuario import Usuario, hash_password  # si necesitas el hash
from usuario import Visitante
from usuario import Artista
from usuario import Moderador
from obras import Obras
from reportes import Reportes
from salas import Salas
from comentarios import Comentarios

import tkinter as tk
import subprocess
import sys
import os