import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='bibutcher',
        tipo='Cliente', 
        nombre='Billy', 
        apellido='Butcher', 
        correo=test_user_email if test_user_email else 'ad.cartes@duocuc.cl', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='123 Main Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/billy.jpg')

    crear_usuario(
        username='rafisher',
        tipo='Cliente', 
        nombre='Ray', 
        apellido='Fisher', 
        correo=test_user_email if test_user_email else 'ad.cartes@duocuc.cl', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='Albert Street, New York, \nNew York 10001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/Rayfisher.jpg')

    crear_usuario(
        username='ezmiller',
        tipo='Cliente', 
        nombre='Ezra', 
        apellido='Miller', 
        correo=test_user_email if test_user_email else 'ad.cartes@duocuc.cl', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='105 Apple Park Way, \nCupertino, CA 95014 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/ezram.jpg')

    crear_usuario(
        username='jamomoa',
        tipo='Cliente', 
        nombre='Jason', 
        apellido='Momoa', 
        correo=test_user_email if test_user_email else 'ad.cartes@duocuc.cl', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='350 5th Ave, \nNew York, NY 10118 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/JasonMomoa.jpg')

    crear_usuario(
        username='gagadot',
        tipo='Administrador', 
        nombre='Gal', 
        apellido='Gadot', 
        correo=test_user_email if test_user_email else 'ad.cartes@duocuc.cl', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='10 Pine Road, Miami, \nFlorida 33101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/Gal_Gadot.jpg')
    
    crear_usuario(
        username='beaffleck',
        tipo='Administrador', 
        nombre='Ben', 
        apellido='Affleck', 
        correo=test_user_email if test_user_email else 'ad.cartes@duocuc.cl', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21.708.052-5', 
        direccion='1600 Pennsylvania Avenue NW, \nWashington, D.C. \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/Ben_affleck.jpg')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='Henry',
        apellido='Cavill',
        correo=test_user_email if test_user_email else 'ad.cartes@duocuc.cl',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='15 Oak Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/henrycavill.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
        { 'id': 5, 'nombre': 'Lucha'},
        { 'id': 6, 'nombre': 'Terror'},
        { 'id': 7, 'nombre': 'Puzzle'},
        { 'id': 8, 'nombre': 'Soulslike'},
        { 'id': 9, 'nombre': 'Ciencia ficción'},
        { 'id': 10, 'nombre': 'Simulador'},
        { 'id': 11, 'nombre': 'Mundo abierto'},
        { 'id': 12, 'nombre': 'Supervivencia'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción" (8 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=11),
            'nombre': 'Forza Horizon 4',
            'descripcion': 'Forza Horizon 4 te lleva a la pintoresca y variada Gran Bretaña, donde explorarás un mundo abierto dinámico que cambia con las estaciones del año. Vive la emoción de las carreras y la exploración en un entorno que se transforma con el clima y la época del año, afectando las carreteras y el paisaje. Conduce más de 450 coches icónicos y participa en una amplia gama de eventos, desde carreras callejeras hasta desafíos de acrobacias. Además, disfruta de un modo multijugador en línea donde puedes competir y colaborar con otros jugadores en tiempo real, creando y compartiendo tus propios eventos y rutas personalizadas. Forza Horizon 4 combina gráficos impresionantes, jugabilidad accesible y una comunidad activa para ofrecer una experiencia de conducción inigualable.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/forza.jpg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'Tekken 8',
            'descripcion': 'Tekken 8 te sumerge en el dinámico y frenético mundo de las artes marciales con su última entrega en la aclamada serie de lucha. Sigue la intensa y emocional historia de la familia Mishima, mientras viejas rivalidades resurgen y nuevos personajes se unen al combate. Disfruta de un sistema de lucha refinado y accesible que mantiene la profundidad estratégica y la diversidad de movimientos que han definido la serie.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/tekken8.webp'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'Street Fighter™ 6',
            'descripcion': 'Street Fighter 6 te invita a sumergirte en el vibrante y competitivo mundo de las artes marciales con su última y esperada entrega. Experimenta la evolución de la franquicia con un nuevo motor gráfico que ofrece combates visualmente deslumbrantes y fluidos, escenarios detallados y animaciones espectaculares.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/street6.webp'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=12),
            'nombre': 'Rust',
            'descripcion': 'Rust te sumerge en un despiadado mundo de supervivencia multijugador donde tu principal objetivo es mantenerse con vida. Empieza sin nada más que una roca y una antorcha, y progresa construyendo refugios, recolectando recursos y fabricando armas. Enfréntate a la dura naturaleza, a los peligrosos animales salvajes y, lo más importante, a otros jugadores que pueden ser aliados o enemigos. Rust ofrece un entorno dinámico donde la cooperación y la traición están a la orden del día, creando una experiencia de juego intensa y llena de adrenalina.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/rust.webp'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=12),
            'nombre': 'ARK: Survival Evolved',
            'descripcion': 'ARK: Survival Evolved te lleva a una misteriosa isla llena de dinosaurios y criaturas prehistóricas. Despiertas sin nada y debes cazar, recolectar recursos, construir refugios y domesticar dinosaurios para sobrevivir. Con un enfoque en la supervivencia, la exploración y la cooperación multijugador, ARK ofrece un mundo inmersivo y vasto donde puedes formar tribus, construir bases impresionantes y enfrentarte a amenazas tanto naturales como humanas. La combinación de ciencia ficción y elementos prehistóricos crea una experiencia única y emocionante.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/ark.webp'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=8),
            'nombre': 'Lies of P',
            'descripcion': 'Lies of P es un oscuro y retorcido juego de acción y rol inspirado en el cuento de Pinocho. Ambientado en una ciudad de pesadilla estilo Belle Époque, sigues a un Pinocho mecánico en su búsqueda por encontrar a Geppetto y descubrir la verdad sobre su propia existencia. Con combates intensos, decisiones morales que afectan la narrativa y un estilo artístico impresionante, Lies of P ofrece una experiencia profunda y atmosférica que desafía tus habilidades y tu percepción de la verdad.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/liesofp.webp'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=11),
            'nombre': 'Hogwarts Legacy',
            'descripcion': 'Hogwarts Legacy te invita a vivir tu propia aventura mágica en el mundo de Harry Potter. Ambientado en el siglo XIX, mucho antes de los eventos de los libros y películas, asumes el papel de un estudiante con habilidades mágicas únicas que llega a Hogwarts. Explora el icónico castillo, asiste a clases de magia, desentraña antiguos misterios y enfréntate a peligrosos enemigos. Con un mundo abierto y rico en detalles, Hogwarts Legacy ofrece una experiencia inmersiva que permite a los fanáticos de la saga vivir su fantasía de ser un mago o bruja.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/hogwarts.webp'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Metro Exodus',
            'descripcion': 'Metro Exodus es un juego de disparos en primera persona que combina elementos de supervivencia y horror en un mundo post-apocalíptico. Sigue la historia de Artyom mientras él y sus compañeros huyen del metro de Moscú en busca de una nueva vida en el este de Rusia. Viaja a través de vastos y peligrosos paisajes, enfrentándote a enemigos mutantes y humanos mientras lidias con condiciones extremas y escasos recursos. Con un enfoque en la narrativa y un mundo abierto que cambia con las estaciones, Metro Exodus ofrece una experiencia intensa y atmosférica.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/metroexodus.jpg'
        },
        # Categoría "Aventura" (4 juegos)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Sea of Thieves',
            'descripcion': 'Sea of Thieves te permite vivir la vida de un pirata en un vasto mundo multijugador en línea lleno de aventuras. Únete a otros jugadores para formar una tripulación, navega por mares traicioneros, busca tesoros escondidos y enfréntate a otros piratas en emocionantes batallas navales. Con un estilo visual único y una jugabilidad centrada en la cooperación y la diversión, Sea of Thieves ofrece una experiencia pirata dinámica y siempre cambiante donde cada sesión de juego puede traer nuevas sorpresas y desafíos.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/seaofthieves.png'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=11),
            'nombre': 'Far Cry Primal',
            'descripcion': 'Far Cry Primal te transporta a la Edad de Piedra, donde asumes el papel de Takkar, un cazador que busca unir a su tribu y sobrevivir en un mundo brutal y salvaje. Explora un vasto y hermoso mundo abierto lleno de peligrosos depredadores y tribus enemigas. Utiliza herramientas primitivas, domestica animales salvajes y lucha por la supervivencia y la dominación en un entorno donde la naturaleza es tanto tu mayor enemigo como tu más valioso aliado. Far Cry Primal ofrece una experiencia única en la serie Far Cry, centrada en la supervivencia y la prehistoria.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/farcry.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=8),
            'nombre': 'Blasphemous 2',
            'descripcion': 'Sumérgete en un mundo oscuro y retorcido en esta secuela del aclamado Blasphemous. Con gráficos mejorados, combates más desafiantes y una narrativa profunda, Blasphemous 2 te invita a explorar un vasto mundo lleno de secretos y peligros. Enfréntate a temibles enemigos y descubre la verdad detrás de la maldición que asola esta tierra. Con un estilo artístico único y una jugabilidad que combina acción y plataformas, Blasphemous 2 ofrece una experiencia inolvidable para los fanáticos del género.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/blas2.webp'
        },
            {
            'id': 12,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'Dragon Ball Fighter Z',
            'descripcion': 'Revive la emoción de las épicas batallas de Dragon Ball en este aclamado juego de lucha. Con gráficos espectaculares y un sistema de combate accesible pero profundo, Dragon Ball Fighter Z te permite controlar a tus personajes favoritos de la serie y enfrentarte a oponentes en intensas peleas llenas de acción.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/fighterz.webp'
        },
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Darkest Dungeon',
            'descripcion': 'Adéntrate en las profundidades de la oscuridad con Darkest Dungeon, un desafiante juego de rol táctico. Lidera a un grupo de héroes imperfectos en misiones peligrosas, gestionando su estrés y sus habilidades mientras te enfrentas a horrores inimaginables. ¿Podrás mantener la cordura mientras desciendes en la locura?',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/darkest.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=6),
            'nombre': 'Dead by Daylight',
            'descripcion': 'Sumérgete en un emocionante juego de terror y supervivencia asimétrico. Juega como uno de los cuatro sobrevivientes que deben escapar de un asesino implacable, o toma el rol del asesino y caza a tus presas. Con un elenco de personajes icónicos del cine de terror, cada partida de Dead by Daylight es una experiencia única y escalofriante.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/deadbyd.webp'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=9),
            'nombre': 'Detroit: Become Human',
            'descripcion': 'Explora una visión futurista de Detroit en este aclamado juego narrativo. Controla a tres androides, cada uno con su propia historia y decisiones que afectarán el destino de la humanidad. Con gráficos impresionantes y una narrativa profunda y emocional, Detroit: Become Human te hará cuestionar la naturaleza de la conciencia y la moralidad.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/detroit.jpg'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=8),
            'nombre': 'Sekiro: Shadows Die Twice',
            'descripcion': 'Embárcate en una intensa aventura de acción en el Japón feudal. En Sekiro: Shadows Die Twice, asumes el rol de un shinobi en busca de venganza y redención. Con un sistema de combate exigente y un mundo detallado, este juego te desafiará a dominar tus habilidades y superar enemigos formidables.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/sekiro.jpg'
        },
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Octopath Traveler',
            'descripcion': 'Descubre un mundo de fantasía encantador en Octopath Traveler. Este RPG presenta un estilo visual único que combina gráficos retro con efectos modernos. Elige entre ocho personajes, cada uno con su propia historia y habilidades, y explora un vasto mundo lleno de aventuras y misterios por descubrir.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/octopath.png'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=10),
            'nombre': 'Stardew Valley',
            'descripcion': 'Escapa del bullicio de la ciudad y construye la granja de tus sueños en Stardew Valley. Este relajante simulador de granja te permite cultivar, criar animales, pescar, explorar minas y formar relaciones con los habitantes del pueblo. Con una jugabilidad profunda y encantadora, Stardew Valley es el refugio perfecto del estrés diario.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/stardew.webp'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=7),
            'nombre': 'We Were Here Forever',
            'descripcion': 'Sumérgete en una experiencia cooperativa en este intrigante juego de puzzles. Tú y un compañero deberán comunicarse y colaborar para escapar de un castillo misterioso lleno de enigmas y desafíos. Con una atmósfera envolvente y rompecabezas ingeniosos, We Were Here Forever pondrá a prueba tu ingenio y trabajo en equipo.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/wewere.jpg'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Slay the Spire',
            'descripcion': 'Embárcate en una aventura roguelike de construcción de mazos en Slay the Spire. Selecciona tus cartas sabiamente y derrota a enemigos en cada nivel mientras asciendes por la torre. Con una jugabilidad adictiva y estratégica, cada partida es una nueva oportunidad para descubrir combinaciones de cartas únicas y desafiarte a ti mismo.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/slay.jpg'
        }
    ]
    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['25.747.200-0', '11.991.600-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

