import sqlite3

class Database:
    
    def __init__(self, db_name='chat.db'):
        self.db_name = db_name
        self.CURRENT_SESION = -1
        
        self.create_tables()
    
    def create_tables(self):
        """Crea las tablas si no existen."""
        with sqlite3.connect(self.db_name) as conn:
            
            # Aplicar cifrado con una clave
            conn.execute("PRAGMA key = 'qwertyHol@0000';")
            
            cursor = conn.cursor()
            
            # Crear tabla 'sesiones'
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sesiones (
                    id_sesion INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    id_usuario INTEGER NOT NULL,  
                    email TEXT NOT NULL,
                    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fuente_datos_externa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT  NOT NULL,
                    key_words TEXT  NOT NULL,  -- Almacena la lista de palabras clave como una cadena separada por comas
                    path_file TEXT NOT NULL
                )
            ''')
            
            # Crear tabla 'conversaciones'
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversaciones (
                    id_conversacion INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_sesion INTEGER NOT NULL,                       -- Identificador de la sesión (clave foránea)
                    role TEXT NOT NULL,                               -- Rol del remitente ('user', 'assistant', o 'function')
                    content TEXT NOT NULL,                            -- Contenido del mensaje
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,        -- Fecha y hora del mensaje
                    FOREIGN KEY (id_sesion) REFERENCES sesiones(id_sesion)
                )
            ''')
            conn.commit()

    def open_conn(self):
        """Abre la conexión con la base de datos."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close_conn(self):
        """Cierra la conexión con la base de datos."""
        if self.conn:
            self.conn.close()

    def create_sesion(self, userId, userEmail):
        """Crea una nueva sesión."""
        try:
            self.open_conn()
            # Insertar nueva sesión
            self.cursor.execute('''
                INSERT INTO sesiones (id_usuario, email, description)
                VALUES (?, ?, ?)
            ''', (userId, userEmail, "Chat Actual"))
            
            # Obtener el último ID insertado
            self.CURRENT_SESION = self.cursor.lastrowid
            print(f"Sesión creada con ID: {self.CURRENT_SESION}")
            self.conn.commit()
        
        except sqlite3.Error as e:
            print(f"Error creando la sesión: {e}")
        finally:
            self.close_conn()

    def insert_conversation(self, id_sesion, role, content):
        """Inserta un mensaje en una conversación."""
        try:
            self.open_conn()
            # Insertar conversación utilizando placeholders para evitar inyección SQL
            self.cursor.execute('''
                INSERT INTO conversaciones (id_sesion, role, content)
                VALUES (?, ?, ?)
            ''', (id_sesion, role, content))
            
            self.conn.commit()
            print("Conversación insertada correctamente.")
        
        except sqlite3.Error as e:
            print(f"Error insertando conversación: {e}")
        finally:
            self.close_conn()
            

    def insert_fuente_datos(self, name, description, key_words, path_file):
   
        try:
            self.open_conn()
            self.cursor.execute('''
                INSERT INTO fuente_datos_externa (name, description, key_words, path_file)
                VALUES (?, ?, ?, ?)
            ''', (name, description, key_words, path_file))
            
            self.conn.commit()
            print("insertada correctamente.")
        
        except sqlite3.Error as e:
            print(f"Error insertando: {e}")
        finally:
            self.close_conn()
            
            
            
    def get_fuentes_externas(self):
        try:
            self.open_conn()
            # Seleccionar todas las conversaciones para la sesión especificada
            self.cursor.execute('SELECT * FROM fuente_datos_externa')
            
            # Obtener el resultado
            fuentes_externas = self.cursor.fetchall()
            print("Fuente datos externa: ", fuentes_externas)             
            
            return fuentes_externas
        
        except sqlite3.Error as e:
            print(f"Error obteniendo conversaciones: {e}")
        finally:
            self.close_conn()              
            
            
    def update_sesion_description(self, id_sesion, new_description):
       
        try:
            self.open_conn()
            # Insertar conversación utilizando placeholders para evitar inyección SQL
            self.cursor.execute('''
                UPDATE sesiones 
                SET description = ?
                WHERE id_sesion = ?
            ''', (new_description, id_sesion))
            
            self.conn.commit()
        
        except sqlite3.Error as e:
            print(f"Error insertando conversación: {e}")
        finally:
            self.close_conn()
            
    def get_conversation(self, id_sesion):
        """Obtiene todas las conversaciones de una sesión."""
        try:
            self.open_conn()
            # Seleccionar todas las conversaciones para la sesión especificada
            self.cursor.execute('''
                SELECT * FROM conversaciones WHERE id_sesion = ?
            ''', (id_sesion,))
            
            conversaciones = self.cursor.fetchall()
            
            conversationObj = []
         
            for c in conversaciones:
                conversationObj.append({"role": f"{c[2]}", "content": f"{c[3]}"})

            return conversationObj
            # Mostrar los resultados
            #for conversacion in conversaciones:
            #    print(conversacion)
            
            #self.CURRENT_SESION = id_sesion
        
        except sqlite3.Error as e:
            print(f"Error obteniendo conversaciones: {e}")
        finally:
            self.close_conn()
            
    def get_last_sesion(self, userId, userEmail):
        "Busca la última sesion del usuario y la asigna a CURRENT_SESION, sino existe la crea."
      
        try:
            self.open_conn()

            self.cursor.execute('''
                SELECT id_sesion FROM sesiones WHERE id_usuario = ? ORDER BY id_sesion DESC LIMIT 1;
            ''', (userId, ))
            
            # Obtener el resultado
            last_session = self.cursor.fetchone()
                        
            if last_session:
                self.CURRENT_SESION = last_session[0]
            else:
                self.create_sesion(userId=userId, userEmail=userEmail)   
        
        except sqlite3.Error as e:
            print(f"Error obteniendo conversaciones: {e}")
        finally:
            self.close_conn()
    
    def get_sesion(self, userId):
        """Obtiene todas las sesione."""
        try:
            self.open_conn()
            # Seleccionar todas las conversaciones para la sesión especificada
            self.cursor.execute('''
                SELECT * FROM sesiones WHERE id_usuario = ? ORDER BY id_sesion DESC;
            ''', (userId, ))
            
            # Obtener el resultado
            session = self.cursor.fetchall()
                        
            
            return session
        
        except sqlite3.Error as e:
            print(f"Error obteniendo conversaciones: {e}")
        finally:
            self.close_conn()        

   
    def delete_sesion(self, id_sesion):
        try:
            self.open_conn()
            # Ejecutar la consulta de eliminación con placeholders para evitar inyección SQL
            self.cursor.execute('''
                DELETE FROM sesiones 
                WHERE id_sesion = ?
            ''', (id_sesion, ))
            
            self.conn.commit()
            
            # Confirmación de eliminación exitosa
            if self.cursor.rowcount > 0:
                print(f"Sesión con id {id_sesion} eliminada exitosamente.")
            else:
                print(f"No se encontró ninguna sesión con id {id_sesion}.")

        except sqlite3.Error as e:
            print(f"Error eliminando la sesión {id_sesion}: {e}")
        finally:
            self.close_conn()
            
   
    def delete_conversation(self, id_sesion):
        try:
            self.open_conn()
            # Ejecutar la consulta de eliminación con placeholders para evitar inyección SQL
            self.cursor.execute('''
                DELETE FROM conversaciones 
                WHERE id_sesion = ?
            ''', (id_sesion, ))
            
            self.conn.commit()
            
            # Confirmación de eliminación exitosa
            if self.cursor.rowcount > 0:
                print(f"conversaciones con id {id_sesion} eliminada exitosamente.")
            else:
                print(f"No se encontró ninguna sesión con id {id_sesion}.")

        except sqlite3.Error as e:
            print(f"Error eliminando la sesión: {e}")
        finally:
            self.close_conn()
            
            
            
    def delete_history(self, userId):
        sesions = self.get_sesion(userId=userId)

        for s in sesions:
            self.delete_conversation(id_sesion=s[0])

        for s in sesions:
            self.delete_sesion(id_sesion=s[0])
        
        return True