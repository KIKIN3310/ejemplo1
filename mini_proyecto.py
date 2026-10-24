class Contacto:
    CATEGORIAS_VALIDAS = ["Familia", "Amigos", "Trabajo", "Estudio", "Otro"]

    def __init__(self, id_contacto: int, nombre: str, telefono: str, correo: str, categoria: str, favorito: bool = False):
        self._id_contacto = id_contacto
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.categoria = categoria
        self.favorito = favorito

    # --- Métodos de validación estáticos (para validar al instante y dentro de setters) ---

    @staticmethod
    def validar_nombre(valor: str) -> str:
        if not valor or not valor.strip():
            raise ValueError("El nombre es obligatorio y no puede estar vacío.")
        return valor.strip()

    @staticmethod
    def validar_telefono(valor: str) -> str:
        limpio = valor.strip().replace(" ", "").replace("-", "")
        if not limpio.isdigit() or len(limpio) < 8 or len(limpio) > 15:
            raise ValueError("El teléfono debe contener solo números (entre 8 y 15 dígitos).")
        return limpio

    @staticmethod
    def validar_correo(valor: str) -> str:
        limpio = valor.strip().lower()
        if " " in limpio or limpio.count("@") != 1:
            raise ValueError("El correo debe contener exactamente un símbolo '@' y sin espacios.")

        usuario, dominio = limpio.split("@")
        if not usuario or not dominio or "." not in dominio:
            raise ValueError("El correo no tiene un dominio válido (ejemplo: usuario@correo.com).")

        partes_dominio = dominio.split(".")
        if any(len(parte) == 0 for parte in partes_dominio):
            raise ValueError("El dominio del correo está incompleto.")
        return limpio

    @classmethod
    def validar_categoria(cls, valor: str) -> str:
        normalizada = valor.strip().capitalize()
        if normalizada not in cls.CATEGORIAS_VALIDAS:
            raise ValueError(f"Categoría no válida. Opciones: {', '.join(cls.CATEGORIAS_VALIDAS)}")
        return normalizada

    # --- Getters y Setters con Encapsulamiento ---

    @property
    def id_contacto(self) -> int:
        return self._id_contacto

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = self.validar_nombre(valor)

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        self._telefono = self.validar_telefono(valor)

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        self._correo = self.validar_correo(valor)

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str):
        self._categoria = self.validar_categoria(valor)

    def actualizar_telefono(self, nuevo_telefono: str):
        self.telefono = nuevo_telefono

    def actualizar_correo(self, nuevo_correo: str):
        self.correo = nuevo_correo

    def alternar_favorito(self):
        self.favorito = not self.favorito

    def mostrar_informacion(self) -> str:
        fav_marca = "*" if self.favorito else " "
        return (
            f"[{fav_marca}] ID: {self._id_contacto:<4} | "
            f"Nombre: {self._nombre:<20} | "
            f"Tel: {self._telefono:<12} | "
            f"Correo: {self._correo:<25} | "
            f"Categoría: {self._categoria}"
        )


class Agenda:
    def __init__(self):
        self._contactos: list[Contacto] = []

    def existe_id(self, id_contacto: int) -> bool:
        return any(c.id_contacto == id_contacto for c in self._contactos)

    def existe_telefono(self, telefono: str, ignorar_id: int = None) -> bool:
        limpio = telefono.strip().replace(" ", "").replace("-", "")
        return any(c.telefono == limpio and c.id_contacto != ignorar_id for c in self._contactos)

    def existe_correo(self, correo: str, ignorar_id: int = None) -> bool:
        limpio = correo.strip().lower()
        return any(c.correo == limpio and c.id_contacto != ignorar_id for c in self._contactos)

    def agregar(self, contacto: Contacto) -> bool:
        # Evitar identificadores, teléfonos o correos duplicados
        if self.existe_id(contacto.id_contacto):
            print(f"[!] Error: El ID {contacto.id_contacto} ya está registrado.")
            return False
        if self.existe_telefono(contacto.telefono):
            print(f"[!] Error: El teléfono {contacto.telefono} ya existe en la agenda.")
            return False
        if self.existe_correo(contacto.correo):
            print(f"[!] Error: El correo {contacto.correo} ya existe en la agenda.")
            return False

        self._contactos.append(contacto)
        return True

    def listar(self) -> list[Contacto]:
        return self._contactos

    def listar_ordenados_por_nombre(self) -> list[Contacto]:
        return sorted(self._contactos, key=lambda c: c.nombre.lower())

    def buscar_por_id(self, id_contacto: int) -> Contacto | None:
        for c in self._contactos:
            if c.id_contacto == id_contacto:
                return c
        return None

    def buscar_por_nombre(self, texto: str) -> list[Contacto]:
        texto = texto.strip().lower()
        return [c for c in self._contactos if texto in c.nombre.lower()]

    def filtrar_por_categoria(self, categoria: str) -> list[Contacto]:
        cat_norm = categoria.strip().capitalize()
        return [c for c in self._contactos if c.categoria == cat_norm]

    def editar_telefono(self, id_contacto: int, nuevo_telefono: str) -> bool:
        contacto = self.buscar_por_id(id_contacto)
        if not contacto:
            print(f"[!] Contacto con ID {id_contacto} no encontrado.")
            return False

        if self.existe_telefono(nuevo_telefono, ignorar_id=id_contacto):
            print(f"[!] El teléfono {nuevo_telefono} ya pertenece a otro contacto.")
            return False

        contacto.actualizar_telefono(nuevo_telefono)
        return True

    def editar_correo(self, id_contacto: int, nuevo_correo: str) -> bool:
        contacto = self.buscar_por_id(id_contacto)
        if not contacto:
            print(f"[!] Contacto con ID {id_contacto} no encontrado.")
            return False

        if self.existe_correo(nuevo_correo, ignorar_id=id_contacto):
            print(f"[!] El correo {nuevo_correo} ya pertenece a otro contacto.")
            return False

        contacto.actualizar_correo(nuevo_correo)
        return True

    def eliminar(self, id_contacto: int) -> bool:
        contacto = self.buscar_por_id(id_contacto)
        if contacto:
            self._contactos.remove(contacto)
            return True
        return False

    def conteo_por_categoria(self) -> dict[str, int]:
        conteo = {cat: 0 for cat in Contacto.CATEGORIAS_VALIDAS}
        for c in self._contactos:
            conteo[c.categoria] += 1
        return conteo


# --- Funciones de Entrada con Validación Inmediata (vuelven a pedir el dato si hay error) ---

def pedir_entero(mensaje: str) -> int:
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor < 0:
                print("[!] Ingresa un número positivo.")
                continue
            return valor
        except ValueError:
            print("[!] Error: Ingresa un número entero válido.")


def pedir_id_unico(agenda: Agenda) -> int:
    while True:
        id_c = pedir_entero("ID: ")
        if id_c == 0:
            print("[!] Error: El ID debe ser mayor a 0.")
        elif agenda.existe_id(id_c):
            print(f"[!] Error: El ID {id_c} ya está registrado. Intenta con otro.")
        else:
            return id_c


def pedir_nombre_valido() -> str:
    while True:
        try:
            return Contacto.validar_nombre(input("Nombre: "))
        except ValueError as e:
            print(f"[!] Error: {e}")


def pedir_telefono_valido(agenda: Agenda, ignorar_id: int = None, mensaje: str = "Teléfono (solo dígitos, 8 a 15): ") -> str:
    while True:
        try:
            tel = Contacto.validar_telefono(input(mensaje))
            if agenda.existe_telefono(tel, ignorar_id=ignorar_id):
                print(f"[!] Error: El teléfono '{tel}' ya existe en la agenda. Ingresa otro.")
                continue
            return tel
        except ValueError as e:
            print(f"[!] Error: {e}")


def pedir_correo_valido(agenda: Agenda, ignorar_id: int = None, mensaje: str = "Correo (ej. nombre@dominio.com): ") -> str:
    while True:
        try:
            correo = Contacto.validar_correo(input(mensaje))
            if agenda.existe_correo(correo, ignorar_id=ignorar_id):
                print(f"[!] Error: El correo '{correo}' ya existe en la agenda. Ingresa otro.")
                continue
            return correo
        except ValueError as e:
            print(f"[!] Error: {e}")


def pedir_categoria_valida() -> str:
    print(f"Categorías: {', '.join(Contacto.CATEGORIAS_VALIDAS)}")
    while True:
        try:
            return Contacto.validar_categoria(input("Categoría: "))
        except ValueError as e:
            print(f"[!] Error: {e}")


def cargar_datos_iniciales(agenda: Agenda):
    contactos_demo = [
        (1, "Astrid Gudiel", "50244112233", "astrid.g@correo.com", "Amigos", False),
        (2, "Byron Sandoval", "50255889900", "byron.s@correo.com", "Amigos", False),
        (3, "Marcelo Crasborm", "50233445566", "marcelo.c@correo.com", "Amigos", False),
        (4, "Joseph Jupeee", "50277881122", "joseph.j@estudio.edu", "Amigos", False),
    ]
    for id_c, nom, tel, mail, cat, fav in contactos_demo:
        agenda.agregar(Contacto(id_c, nom, tel, mail, cat, fav))


def imprimir_menu():
    print()
    print("1. Agregar contacto")
    print("2. Mostrar todos los contactos")
    print("3. Buscar contacto por ID")
    print("4. Buscar contacto por nombre")
    print("5. Modificar teléfono")
    print("6. Modificar correo")
    print("7. Mostrar contactos por categoría")
    print("8. Eliminar contacto")
    print("9. Ordenar contactos alfabéticamente")
    print("10. Marcar / desmarcar como favorito (*)")
    print("11. Reporte de contactos por categoría")
    print("0. Salir")


def main():
    agenda = Agenda()
    cargar_datos_iniciales(agenda)

    while True:
        imprimir_menu()
        opcion = pedir_entero("Selecciona una opción: ")

        if opcion == 1:
            print("\n--- AGREGAR CONTACTO ---")
            id_c = pedir_id_unico(agenda)
            nom = pedir_nombre_valido()
            tel = pedir_telefono_valido(agenda)
            mail = pedir_correo_valido(agenda)
            cat = pedir_categoria_valida()

            nuevo = Contacto(id_c, nom, tel, mail, cat)
            if agenda.agregar(nuevo):
                print("Contacto guardado con éxito.")

        elif opcion == 2:
            print("\n--- LISTA DE CONTACTOS ---")
            contactos = agenda.listar()
            if not contactos:
                print("La agenda está vacía.")
            else:
                for c in contactos:
                    print(c.mostrar_informacion())

        elif opcion == 3:
            id_busq = pedir_entero("ID a buscar: ")
            contacto = agenda.buscar_por_id(id_busq)
            if contacto:
                print("\nContacto encontrado:")
                print(contacto.mostrar_informacion())
            else:
                print(f"[!] Contacto con ID {id_busq} no encontrado.")

        elif opcion == 4:
            texto = input("Nombre o fragmento a buscar: ").strip()
            resultados = agenda.buscar_por_nombre(texto)
            if resultados:
                print(f"\nSe encontraron {len(resultados)} contacto(s):")
                for c in resultados:
                    print(c.mostrar_informacion())
            else:
                print(f"[!] No se encontró ningún contacto con '{texto}'.")

        elif opcion == 5:
            id_c = pedir_entero("ID del contacto a modificar: ")
            contacto = agenda.buscar_por_id(id_c)
            if contacto:
                nuevo_tel = pedir_telefono_valido(
                    agenda,
                    ignorar_id=id_c,
                    mensaje=f"Nuevo teléfono para {contacto.nombre}: "
                )
                if agenda.editar_telefono(id_c, nuevo_tel):
                    print("Teléfono actualizado.")
            else:
                print(f"[!] Contacto con ID {id_c} no encontrado.")

        elif opcion == 6:
            id_c = pedir_entero("ID del contacto a modificar: ")
            contacto = agenda.buscar_por_id(id_c)
            if contacto:
                nuevo_mail = pedir_correo_valido(
                    agenda,
                    ignorar_id=id_c,
                    mensaje=f"Nuevo correo para {contacto.nombre}: "
                )
                if agenda.editar_correo(id_c, nuevo_mail):
                    print("Correo actualizado.")
            else:
                print(f"[!] Contacto con ID {id_c} no encontrado.")

        elif opcion == 7:
            cat = pedir_categoria_valida()
            filtrados = agenda.filtrar_por_categoria(cat)
            if filtrados:
                print(f"\n--- Contactos en '{cat}' ---")
                for c in filtrados:
                    print(c.mostrar_informacion())
            else:
                print(f"No hay contactos registrados en '{cat}'.")

        elif opcion == 8:
            id_c = pedir_entero("ID del contacto a eliminar: ")
            if agenda.eliminar(id_c):
                print(f"Contacto con ID {id_c} eliminado correctamente.")
            else:
                print(f"[!] Contacto con ID {id_c} no encontrado.")

        elif opcion == 9:
            print("\n--- CONTACTOS ORDENADOS ALFABÉTICAMENTE ---")
            for c in agenda.listar_ordenados_por_nombre():
                print(c.mostrar_informacion())

        elif opcion == 10:
            id_c = pedir_entero("ID del contacto para cambiar favorito: ")
            contacto = agenda.buscar_por_id(id_c)
            if contacto:
                contacto.alternar_favorito()
                estado = "marcado como favorito" if contacto.favorito else "desmarcado de favoritos"
                print(f"{contacto.nombre} fue {estado}.")
            else:
                print(f"[!] Contacto con ID {id_c} no encontrado.")

        elif opcion == 11:
            print("\n--- REPORTE POR CATEGORÍA ---")
            conteo = agenda.conteo_por_categoria()
            for cat, cant in conteo.items():
                print(f"• {cat:<10}: {cant}")
            print(f"Total en agenda: {len(agenda.listar())}")

        elif opcion == 0:
            print("\nBye byeeeeeee 10/10 va inge")
            break
        else:
            print("[!] Opción no reconocida.")


if __name__ == "__main__":
    main()