from django.db import models

STATUS_CHOICES = (
    ('draft', 'draft'),
    ('review', 'review'),
    ('rejected', 'rejected'),
    ('need_changes', 'need changes'),
    ('published', 'published')
)

REVIEW_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('completed', 'Completed')
)

POST_TYPE_CHOICES = (
    ('embeded', 'embeded'),
    ('youtube', 'youtube')
)


class Post(models.Model):
    """
    Post Model

    Post has some properties related to a post on a web, a generic container for content in Afinidata.

    Args:
        name: Nombre del post.
        status: Puede ser: draft, review, rejected, need_changes, published. Donde “draft” representa que aún está en borrador, “review” que se encuentra en revisión, “rejected” que ha sido rechazado, “need_changes” que hay cambios por realizar y “published”, que representa que el servicio que distribuye los posts lo tomará en cuenta.
        type: Puede ser: embeded, youtube. Donde embeded muestra en un iframe que ocupa toda la pantalla el contenido de un link, y youtube muestra un vídeo de youtube a través de su ID. (Próximo paso, un editor WYSIWYG y un type extra llamado “content”).
        content: Dependiendo del type, debería ser un link en el type “embeded”, y el ID del vídeo de Youtube en el type “youtube”. (Próximo paso, contenido resultante del editor WYSIWYG en el type “content”).
        content_activity: Contenido que es enviado al usuario del bot cuando este por problemas de conexión no puede ver el enlace o el vídeo del post. Se utiliza este signo “|” para delimitar el contenido de cada mensaje a través del chatbot.
        user: Usuario creador del post.
        min_range: El servicio que devuelve actividades se basa en un value para devolver un post dentro del rango, si value es mayor a este atributo el post es candidato para ser enviado.
        max_range: El servicio que devuelve actividades se basa en un value para devolver un post dentro del rango, si value es menor a este atributo el post es candidato para ser enviado.
        preview: El servicio que devuelve actividades, devuelve un pequeño resumen de qué trata esta actividad para llamar la atención del usuario, es este atributo.
        new (Por eliminar): Delimitaba en cierta fecha si el servicio debía de tomar en cuenta el post para enviarse a usuarios.
        thumbnail: El servicio que devuelve actividades, devuelve una imagen relacionada a la actividad. La url de la imagen debe guardarse en este atributo.
        area_id (Para uso próximo): En idea, guarda el id del área al que pertenecen (Áreas basadas en el proyecto Core (cognitivo, motor, emocional)). Para que el servicio basado en el área solicitada devuelva únicamente posts de esa área. Por defecto se están solicitando a través del chatbot únicamente posts con área 1, mismo valor que se está guardando automáticamente en el modelo.
        created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).
    """
    name = models.CharField(max_length=255)
    status = models.CharField(choices=STATUS_CHOICES, max_length=255, default='draft')
    type = models.CharField(max_length=255, default='embeded', choices=POST_TYPE_CHOICES)
    content = models.TextField()
    content_activity = models.TextField()
    user = models.IntegerField(null=True)
    min_range = models.IntegerField(null=True, default=0)
    max_range = models.IntegerField(null=True, default=72)
    preview = models.TextField()
    new = models.BooleanField(default=False)
    thumbnail = models.TextField()
    area_id = models.IntegerField(null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Interaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user_id = models.IntegerField(default=0)
    username = models.CharField(max_length=255, null=True)
    channel_id = models.CharField(default="", max_length=50)
    bot_id = models.IntegerField(default=1)
    type = models.CharField(max_length=255, default='open')
    value = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.channel_id


class Feedback(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user_id = models.IntegerField(default=0)
    username = models.CharField(max_length=255, null=True)
    channel_id = models.CharField(default="", max_length=50)
    bot_id = models.IntegerField(default=1)
    value = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.channel_id


class Label(models.Model):
    """
    Label

    Args:
        name: Nombre de la categoría
        posts: Referencia de muchos a muchos con el modelo Posts.
        created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).
    """
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Question:

    Args:
        name: Texto de pregunta que le llega al usuario (si se solicita a través de un servicio).
        Post: Referencia al post que pertenece esa pregunta.
        Replies (Por eliminar): Casilla de texto que guardaba las posibles respuestas a una pregunta.
        created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).
    """
    name = models.CharField(max_length=255, unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    replies = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Response(models.Model):
    """
    Response:

    Args:
        question: Referencia a la question respondida.
        user_id: ID del usuario del bot que respondió a la pregunta.
        username: Username del usuario del bot que respondió la pregunta.
        response: Respuesta del usuario a la pregunta.
        created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    response = models.TextField(null=True)
    response_text = models.TextField(null=True)
    response_value = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


# https://anthonyfox.io/posts/choices-for-choices-in-django-charfields
# https://docs.djangoproject.com/en/2.2/ref/models/instances/#django.db.models.Model.get_FOO_display

AREA = [
    ('cogni', 'Cognitivo & Lenguaje'),
    ('motor', 'Motor'),
    ('socio', 'Socioemocional'),
]

SUBAREA = [
    ('lang', "Lenguaje"),
    ('soc', "Socioemocional"),
    ('premath', "Prematemática"),
    ('sensor', "Sensorial"),
    ('motof', "Motricidad Fina"),
    ('motol', "Motricidad Gruesa"),
    ('sci', "Ciencias"),
    ('art', "Arte & Cultura"),
]

COMPONENTS = [
    ("vocabulario", "Vocabulario"),
    ("articulacionfonetica", "Articulación y Fonética"),
    ("sintaxiscomunicacion", "Sintaxis/Comunicación"),
    ("lectoescritura", "Lectoescritura"),
    ("literatura", "Literatura"),
    ("autoconocimiento", "Autoconocimiento"),
    ("autonomia", "Autonomía y Vida Práctica"),
    ("autocontrol", "Autocontrol"),
    ("empatia", "Empatía"),
    ("hsocial", "Habilidades Sociales"),
    ("plogico", "Pensamiento Lógico"),
    ("numconteo", "Números y Conteo"),
    ("problemasOperacionesRazonamiento", "Resolución de Problemas y Operaciones / Razonamiento"),
    ("pVisual", "Percepción Visual"),
    ("pAuditiva", "Percepción Auditiva"),
    ("pHaptica", "Percepción háptica"),
    ("pGustativa", "Percepción Gustativa"),
    ("pOlfativa", "Percepción Olfativa"),
    ("egnostico", "Estereognóstico"),
    ("om", "Coordinación Ojo-Mano"),
    ("pinza", "Movimiento de Pinza"),
    ("desplaza", "Desplazamiento"),
    ("balance", "Balance-Equilibrio"),
    ("tono", "Fuerza-Tonicidad Muscular"),
    ("coordinacion", "Coordinación"),
    ("experimentos", "Experimentos"),
    ("botanica", "Botánica"),
    ("zoologia", "Zoología"),
    ("astronomia", "Astronomía"),
    ("cuidadomh", "Cuidado del Medio Ambiente"),
    ("medionatural", "Medio Natural"),
    ("tech", "Tecnología"),
    ("geo", "Geografía"),
    ("plasticas", "Artes Plásticas"),
    ("musik", "Música"),
    ("danzaTeatro", "Danza y Teatro"),
    ("culturas", "Culturas del Mundo"),
]


class Area(models.Model):
    id = models.CharField(max_length=35, primary_key=True, choices=AREA)
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class Subarea(models.Model):
    id = models.CharField(max_length=35, primary_key=True, choices=SUBAREA)
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class Componente(models.Model):
    id = models.CharField(max_length=35, primary_key=True, choices=COMPONENTS)
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name

class Taxonomy(models.Model):
    post = models.OneToOneField(Post,
                                on_delete=models.CASCADE,
                                primary_key=False,
                                )

    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)
    subarea = models.ForeignKey(Subarea, on_delete=models.DO_NOTHING)
    component = models.ForeignKey(Componente, on_delete=models.DO_NOTHING)


RESPONSE_VALUE_CHOICES = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4))


class QuestionResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.CharField(max_length=255)
    value = models.IntegerField(choices=RESPONSE_VALUE_CHOICES)

    def __str__(self):
        return "%s__%s__%s__%s" % (self.pk, self.question.pk, self.response, self.value)


class MessengerUserCommentPost(models.Model):
    user_id = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s__%s__%s" % (self.pk, self.post_id, self.user_id)


class Tip(models.Model):
    title = models.CharField(max_length=140)
    min_range = models.IntegerField(null=True, default=0)
    max_range = models.IntegerField(null=True, default=72)
    topic = models.CharField(max_length=255)
    tip = models.TextField()


class PostComplexity(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    months = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    complexity = models.CharField(max_length=100)

