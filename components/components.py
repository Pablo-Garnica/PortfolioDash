#___________________________________________________________________________________________
import dash_bootstrap_components as dbc
from dash import html,Output,Input,State
from dash.dependencies import Component
from collections.abc import Callable
from typing import List, Union
"""
decripcion
Args:
    name_t: Nombre del DataFrame
Returns:
    DataFrame con las tranaformaciones descritas
"""
#___________________________________________________________________________________________
def callback_default(app):
    pass
def sumary_name(name):
    ls_n = name.split(" ")
    ls_n = [l[0] for l in ls_n[:2]]
    name = ''.join(ls_n)
    return name
#___________________________________________________________________________________________
class DashComponent():
    """
    Esta clase es para juntar las 2 parter importantes de un componente
    Callback y Layout que junto es una componente
    El objetivo es reutilizar las componentes de forma facil
    Cada componente debe tener un nombre y no se acceden a los atributos
    desde una instancia de clase
    """
    #______________________________________________________________________________________
    def __init__(
            self,
            name,
            layout:Component=html.Div(''),
            callback:Callable=callback_default,
            ) -> None:
        """
        Argumentos para la construccion de la clase desde la inicializacion
        Args:
            name: Nombre de la componente 
            layout: Objeto de tipo dash.dependencies.Component aqui tenemos la parte del
            componente HTML (o dbc si se usa bootstrap)
            callback: Objeto de tipo Callable debe tener el decorador app.callback de dash,
            debe tener un argumento app y realizar la interaccion como un callback de dash
            normal
        Returns:
            None
        """
        self._name = name
        self._layout = layout
        self._callback = callback
    #_______________________________________________________________________________________
    def update_name(self,name:str):
        """
        Actualizacion del nombre
        Args:
            name: Nuevo nombre de la componente
        Returns:
            None
        """
        self._name = name
    #_______________________________________________________________________________________
    def update_layout(self,layout:Component):
        """
        Actualizacion de layout
        Args:
            layout: Objeto de tipo dash.dependencies.Component que actualiza el layout
        Returns:
            None
        """
        self._layout = layout
    #_______________________________________________________________________________________
    def update_callback(self,callback:Callable):
        """
        Actualizacion de callback
        Args:
            callback: Objeto de tipo Callable que actualiza el callback debe tener el decorador 
            app.callback de dash y debe tener un argumento app
        Returns:
            None
        """
        self._callback = callback
    #_______________________________________________________________________________________
    def get_layout(self):
        """
        Obtener de layout
        Args:
            None
        Returns:
            layout
        """
        return self._layout
    #_______________________________________________________________________________________
    def get_callback(self):
        """
        Obtener de callback
        Args:
            None
        Returns:
            callback
        """
        return self._callback
    #_______________________________________________________________________________________
    #Ver los componentes
    def get_name(self):
        """
        Obtener de name
        Args:
            None
        Returns:
            name
        """
        return self._name
#___________________________________________________________________________________________
#Tipos de datos que acepta la clase DashCompGroup
type_comp = Union[List[DashComponent],DashComponent,None]
error_t_comp = TypeError(f'arg: components should be List[DashComponent], DashComponent or None')
def comp_dict_error(components:List[DashComponent]):
    """
    Valida que components cumpla 2 cosas:
    -Que cada elemento de la lista sea un instancia de DashComponent
    -No haya nombres duplicados en las componentes
    Args:
        components: Lista de instancias de DashComponent
    Returns:
        dict_components diccionario que contiene las componentes de la lista
        con key=_name y value = componente (Instancia de DashComponent)
    """
    dict_components = {}
    ls_names = []
    for comp in components:
        #Valida si es instancia de DashComponent
        if isinstance(comp, DashComponent):
            #Valida si hay duplicados y da error en caso de un duplicado
            if comp._name in ls_names:
                raise RuntimeError(f'Duplicate name in components, name duplicate is : {comp._name}')
            else:
                #Agrega la componente
                dict_components.update({comp._name:comp})
            ls_names = ls_names + [comp._name]
        else:
            raise error_t_comp
    return dict_components
#___________________________________________________________________________________________
class DashCompGroup():
    """
    Esta clase sirve para juntar en un objeto instancias de la clase y mandar a llamarlas
    de forma facil y clara
    """
    #_______________________________________________________________________________________
    def __init__(
            self,
            name,
            components:type_comp = None,
            ) -> None:
        """
        Argumentos para la construccion de la clase desde la inicializacion
        Args:
            name: Nombre del grupo de componentes
            components: Instancia de DashComponent o lista de instancias de DashComponent
        Returns:
            None
        """
        self._name = name
        #Si se asigana el valor por default del argumento components
        if components == None:
            self._components = {}
        #Valida si es instancia de DashComponent
        elif isinstance(components, DashComponent):
            #Agrega la componente
            self._components = {components._name:components}
        #Valida si es una lista de instancias de DashComponent
        elif isinstance(components, list):
            self._components = comp_dict_error(components)
        #Si no es de los tipos de datos que queremos lanza error
        else:
            raise error_t_comp
    #_______________________________________________________________________________________
    #Agrega la componente
    def add_component(
            self, 
            components:type_comp,
            ):
        """
        Agrega componentes al grupo de componentes
        Args:
            components: Instancia de DashComponent o lista de instancias de DashComponent
        Returns:
            None
        """
        #Valida si es instancia de DashComponent
        if isinstance(components, DashComponent):
            #Se guarda en update_comp
            update_comp = {components._name:components}
        #Valida si es una lista de instancias de DashComponent
        elif isinstance(components, list):
            #Se guarda en update_comp si pasa las validaciones de lista de componentes
            update_comp = comp_dict_error(components)
        #Si no es de los tipos de datos que queremos lanza error
        else:
            raise error_t_comp
        #Intesecta el conjunto de nombres de la lista de componentes y la lista de nombres
        #del grupo de componentes
        intersection = list(set(update_comp.keys()) & set(self._components.keys()))
        #Manejo de errores para duplicados
        #Si la intersección es mayor a 0 entonces imprime los primeros 10 nombres duplicados
        if len(intersection) > 0 :
            l = min(len(intersection),10)
            int_message = ', '.join(intersection[:l])
            message = f'First {l} of {len(intersection)} duplicate component names: {int_message}'
            raise RuntimeError(message)
        # Si la intersección es vacia actualiza los componentes
        else:
            self._components.update(update_comp)
    #_______________________________________________________________________________________
    #Metodo para exportar en una lista de componentes que se pueden agregar en una clase DashCompGroup
    def to_list(self, prefix = ''):
        ls_names = list(self._components.keys)
        ls_comp = []
        for name in ls_names:
            comp = self._components[name]
            comp.name = f'{prefix}_{name}'
            ls_comp = ls_comp + [comp]
        return ls_comp
    #_______________________________________________________________________________________
    #Ver los componentes
    def get_components(self):
        """
        Obtener diccionario de componentes
        Args:
            None
        Returns:
            components
        """
        return self._components
    #_______________________________________________________________________________________
    #Ver los componentes
    def get_name(self):
        """
        Obtener de name
        Args:
            None
        Returns:
            name
        """
        return self._name
#___________________________________________________________________________________________
class DashModal(DashComponent):
    """
    Es una componente (clase heredada de DashComponent), para crear un modal de herramientas
    Para mostrar 3 fucnionalidades:
    -Panel de filtros, aqui tenemos los filtros globales en la pagina del dashboard
    -Navegación: para elegir la pagina y cambiar de pagina (un router)
    -Informacion: Panel de informacion de la pagina si es que hay alguna especificacion
    """
    def __init__(
            self,
            filter:DashComponent,
            info:DashComponent,
            nav:DashComponent,
            name='modal',
            layout:Component=html.Div(''),
            callback:Callable=callback_default,
            ) -> None:
        """
        Argumentos para la construccion de la clase desde la inicializacion
        Args:
            filter:Componente (instancia de DashComponent) que mostrara el contenido en la
            seccion Filtros
            info:Componente (instancia de DashComponent) que mostrara el contenido en la
            seccion Informacion
            nav:Componente (instancia de DashComponent) que mostrara el contenido en la
            seccion Navegacion
            name:Nombre de componente
            layout: Objeto de tipo dash.dependencies.Component aqui tenemos la parte del
            componente HTML (o dbc si se usa bootstrap)
            callback: Objeto de tipo Callable debe tener el decorador app.callback de dash,
            debe tener un argumento app y realizar la interaccion como un callback de dash
            normal
        Returns:
            None
        """
        super().__init__(name,layout, callback)
        filter.update_name('filter')
        info.update_name('info')
        nav.update_name('nav')
        self.group =  DashCompGroup(
            name="modal",
            components=[filter,info,nav]
        )
        def get_callback(app):
            """
            Crea el un callback para el funcionamiento del modal y agrega los callbacks
            de las componentes filtros, Navegacion e informacion
            Args:
                app: Es el app que se genera a partir de una instancia de dash.Dash
            Returns:
                Funcion callback
            """
            @app.callback(
                Output("tools-modal", "is_open"),
                [Input("tools-open", "n_clicks"), Input("tools-close", "n_clicks"),Input("tools-header-close", "n_clicks")],
                [State("tools-modal", "is_open")],
            )
            def toggle_modal(n1, n2, n3, is_open):
                if n1 or n2 or n3:
                    return not is_open
                return is_open
            @app.callback(
                    [
                        Output("tools-content-select", "children"),
                        Output("tools-header", "children"),
                    ], 
                    [
                        Input("tools-group-button", "value")
                    ]
                    )
            def display_value(value):
                if value==1:
                    layout = self.group.get_components()['filter'].get_layout()
                    return layout, "Filtro"
                elif value==2:
                    layout = self.group.get_components()['nav'].get_layout()
                    return layout, "Navegación"
                elif value==3:
                    layout = self.group.get_components()['info'].get_layout()
                    return layout, "Información"
                else:
                    pass
            #Junta todos los CallBacks en 1
            components = self.group.get_components()
            for name in components.keys():
                call = components[name].get_callback()
                call(app)
            return
        self.update_callback(get_callback)
        #Construye el layout con configuraciones por default
        self.tools()
    def tools(
            self,
            header = None,
            content = None,
            style_header = None ,
            style_button = None ,
            style_button_select = None ,
            bg_color = "#EEEEEE",
            tooltip_button = "Herramientas",
            ):
        """
        Crea un boton de con tooltip del cual al dar click aparece el modal
        Args:
            header: Objeto dash.Component que nuestra el contenido del header
            content: Objeto dash.Component que nuestra el contenido del modal
            tooltip_button: Texto que aparece en el tooltip del boton
        Returns:
            Objeto dash.Component que contiene un boton que activa el modal
        """
        #Si no se pasan argumentos se crean con metodos de la clase
        if style_header == None:
            style_header = {
                'background-color': "#234567",
                'color':'#FFFFFF'
            }
        if style_button == None:
            style_button = {
                'background-color': '#203864',
                'color':'#FFFFFF',
                'border-color':'#FFFFFF'
            }
        if style_button_select == None:
            style_button_select = {
                'background-color': '#3964B1',
                'color':'#FFFFFF',
                'border-color':'#FFFFFF'
            }
        content = self._tools_content(style_button=style_button,style_button_select=style_button_select) if content == None else content
        header = self._header_modal() if header == None else header
        #Cracion del botion del modal
        button_modal = dbc.Button(children=[
            html.I(className="bi bi-wrench"),
                ], 
                id="tools-open",
                color="danger",
                )
        #Creacion del layout del header
        modal_header = dbc.ModalHeader(
            children=[
                header,
                #Boton para cerrar modal 
                dbc.Button(
                children=html.I(className="bi bi-x-lg"),
                id="tools-header-close",
                className="ms-auto",
                n_clicks=0,
                color='danger',
            ),
                ], 
            close_button=False,
            style = style_header
            )
        modal_body = dbc.ModalBody(
            children = [
                content,
            ],
            style={
                'padding':'0px 10px',
                'background-color':bg_color,
            }
            )
        
        modal_footer = dbc.ModalFooter(
            dbc.Button(
                "Cerrar",
                id="tools-close",
                className="ms-auto",
                n_clicks=0,
                style =style_button
            ),
            style={
                'background-color':bg_color,
            }
        )
        #Creacion del tooltip
        tooltip = dbc.Tooltip(
            tooltip_button,
            target= "tools-open",
            placement='bottom',
        )
        #Creacion del modal
        modal = html.Div(
            [
                button_modal,
                dbc.Modal(
                    [
                        modal_header,
                        modal_body,
                        modal_footer,
                    ],
                    id="tools-modal",
                    centered=True,
                    is_open=False,
                    size="lg",
                ),
                tooltip
            ]
        )
        self.update_layout(modal)
        return modal
    #______________________________________________________
    def _tools_content(self,style_button,style_button_select):
        """
        Crea un estilo predeterminado de contenido
        Args:
            None
        Returns:
            Objeto dash.Component que muestra el contenido del modal
        """
        group_button = dbc.RadioItems(
            id="tools-group-button",
            className="btn-group",
            input_class_name="btn-check",
            label_class_name="btn btn-outline-primary",
            label_checked_class_name="active",
            #Estilo de todos los botones no activos
            label_style=style_button,
            #Estilo del boton activo
            label_checked_style=style_button_select,
            options=[
                {"label": "Filtros", "value": 1},
                {"label": "Navegación", "value": 2},
                {"label": "Información", "value": 3},
            ],
            value=1,
        )
        group_button = html.Div(
            group_button,
            style={
                'text-align': 'center',
                'padding':'7.5px 0px',
            }
        )
        content = html.Div(
            [   
                group_button,
                html.Div(
                    id="tools-content-select",
                    style={
                        'padding': '0px 0px',
                    }
                    ),
            ],
            className="radio-group",
        )
        return content
    
    def _header_modal(self):
        """
        Crea un estilo predeterminado del header dbc.Modal
        Args:
            None
        Returns:
            Objeto dash.Component que muestra el contenido del header del modal
        """
        return dbc.ModalTitle(id="tools-header",)
#___________________________________________________________________________________________
class DashAvatar(DashComponent):
    """
    Es una componente (clase heredada de DashComponent), un boton de usuario el cual
    al dar click tienes opciones, lo puedes dividir en grupos de opciones
    """
    def __init__(
            self,
            name_user,
            ls_button=[],
            name='avatar',
            layout:Component=html.Div(''),
            callback:Callable=callback_default,
            ) -> None:
        """
        Argumentos para la construccion de la clase desde la inicializacion
        Args:
            name_user: El nombre completo del usuario
            ls_button: Lista de grupos de botones para el menu desplegable
            name:Nombre de componente
            layout: Objeto de tipo dash.dependencies.Component aqui tenemos la parte del
            componente HTML (o dbc si se usa bootstrap)
            callback: Objeto de tipo Callable debe tener el decorador app.callback de dash,
            debe tener un argumento app y realizar la interaccion como un callback de dash
            normal
        Returns:
            None
        """
        super().__init__(name,layout, callback)
        self._name_user = name_user
        self._ls_button = ls_button
        self._avatar_buton()
        def get_callback(app):
            """
            Crea el un callback para el funcionamiento del modal y agrega los callbacks
            de las componentes filtros, Navegacion e informacion
            Args:
                app: Es el app que se genera a partir de una instancia de dash.Dash
            Returns:
                Funcion callback
            """
        pass
        self.update_callback(get_callback)
    
    def _layout_options(self):
        """
        Metodo interno en la clase la cual formatea el menu del boton de avatar
        actualiza el layout de la clase con el componente de avatar
        Args:
            None
        Returns:
            None
        """
        ls =[
            dbc.Row(html.Div(self._name_user))
        ]
        for group in self._ls_button:
            ls = ls + [
                html.Div(
                    children=group,
                    style={
                        'display': 'flex',
                        'flex-direction': 'column',
                    }
                ),
                html.Hr(style={'border-top': '3px solid #bbb','margin':'5px'}),
            ]
        ls = ls + [
            dbc.Button(
                "Cerrar sesión",
                style={'border-radius':'0px','border': '0'},
                color="light",
                id='logout'
                ),
        ]
        return ls
    def _avatar_buton(self):
        """
        Metodo interno en la clase el cual construye el layout del boton
        Args:
            None
        Returns:
            Componente de avatar
        """
        name_s = sumary_name(self._name_user)
        component = dbc.Button(
            children = html.Div(
            children=html.Div(name_s),
            style={
                'display': 'flex',
                'text-align':'center',
                'justify-content': 'center',
                'align-items': 'center',
                'height':"40px",
                'width':"40px",
                },
        ),
        color="primary",
        style={
            'border-radius': '50%',
            'height':"40px",
            'width':"40px",
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'padding':'0',
            'border':'0'
        },
        id="avatar",
        n_clicks=0,
        )
        component = html.Div(
            [
                component,
                dbc.Popover(
                    [
                        dbc.PopoverBody(
                            dbc.Container(
                            children= self._layout_options(),
                            style={'padding':'10px 12px'},
                        ),
                        style={'padding':'0px'},
                        )
                    ],
                    target="avatar",
                    trigger="legacy",
                    placement="bottom",
                    style={
                        'padding':'0px'
                    },
                ),
            ]
        )
        self.update_layout(component)
#___________________________________________________________________________________________
class DashNavBar(DashComponent):
    """
    Es una componente (clase heredada de DashComponent), crea una componente de NaV bar
    la cual tiene 3 elementos
    -Nombre y logo
    -Modal
    -Avatar
    """
    def __init__(
            self,
            name_app,
            logo_app,
            modal:DashModal = None,
            avatar:DashAvatar = None,
            name='navBar',
            layout:Component=html.Div(''),
            callback:Callable=callback_default,
            ) -> None:
        """
        Argumentos para la construccion de la clase desde la inicializacion
        Args:
            name_app: El de la aplicacion
            logo_app: Imagen del logo de la aplicacion
            modal:Componente modal
            avatar:Componenete de avatar de usuario
            layout: Objeto de tipo dash.dependencies.Component aqui tenemos la parte del
            componente HTML (o dbc si se usa bootstrap)
            callback: Objeto de tipo Callable debe tener el decorador app.callback de dash,
            debe tener un argumento app y realizar la interaccion como un callback de dash
            normal
        Returns:
            None
        """
        super().__init__(name,layout, callback)
        self._name_app = name_app
        self._logo_app = logo_app
        self._modal =  DashComponent('modal') if modal is None else modal
        self._avatar = DashComponent('avatar') if avatar is None else avatar
        def get_callback(app):
            """
            Crea el un callback para el funcionamiento del modal y agrega los callbacks
            de las componentes filtros, Navegacion e informacion
            Args:
                app: Es el app que se genera a partir de una instancia de dash.Dash
            Returns:
                Funcion callback
            """
            self._avatar.get_callback()(app)
            self._modal.get_callback()(app)
            
        self.update_callback(get_callback)
        self.update_layout(self._navBar())

    def _navBar(self):
        """
        Metodo interno el cual crea la componenete Nav Bar
        Args:
            None
        Returns:
            Componenete NavBar
        """
        navbar = dbc.Navbar(
            dbc.Container(
                children=[
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=self._logo_app, height="30px")),
                            dbc.Col(dbc.NavbarBrand(self._name_app, className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    html.Div(
                        children=[
                            self._modal.get_layout(),
                            self._avatar.get_layout(),
                            ],
                        style={
                            'display': 'flex',
                            'gap': '10px'
                        }
                    ),
                ],
                style={
                    'margin-right': '2%',
                    'margin-left': '2%',
                    'max-width': 'none',
                    }
            ),
            color="dark",
            dark=True,
            style={
                'position': 'fixed',
                'top': '0',
                'width': '100%',
            }
        )
        return navbar
#___________________________________________________________________________________________
class DashCard(DashComponent):
    """
    Es una componente (clase heredada de DashComponent), crea un contenedor
    De tipo carta, en la cual tiene encabezado, cuerpo y footer
    """
    #______________________________________________________
    def __init__(
            self,
            header_layout=None,
            header_style={},
            body_layout=None,
            body_style={},
            footer_layout=None,
            footer_style={},
            card_style={},
            name='card',
            layout:Component=html.Div(''),
            callback:Callable=callback_default,
            ) -> None:
        """
        Argumentos para la construccion de la clase desde la inicializacion
        Args:
            header_layout: Componente de dash la cual se insertará en el encabezado
            header_style: Estilos para el encabezado
            body_layout: Componente de dash la cual se insertará en el cuerpo
            body_style: Estilos para el cuerpo
            footer_layout: Componente de dash la cual se insertará en el footer
            footer_style: Estilos para el footer
            card_style: Estilos para el componente completo
            name: Nombre de la componenente
            layout: Objeto de tipo dash.dependencies.Component aqui tenemos la parte del
            componente HTML (o dbc si se usa bootstrap)
            callback: Objeto de tipo Callable debe tener el decorador app.callback de dash,
            debe tener un argumento app y realizar la interaccion como un callback de dash
            normal
        Returns:
            None
        """
        #______________________________________________________
        super().__init__(name,layout, callback)
        #Llama el metodo para la construcción de la componente
        self.card(
            header_layout=header_layout,
            header_style=header_style,
            body_layout=body_layout,
            body_style=body_style,
            footer_layout=footer_layout,
            footer_style=footer_style,
            card_style=card_style,
        )
        #______________________________________________________
    
    def _titles(self,layout=None,style={},type_header=True):
        """
        Metodo para la creación del encabezado o el footer
        Args:
            layout: El contenido que va a tener la componente
            style: Diccionerios de estilos que se le agregan al componente
            type_header: Booleano que indica si es encabezado en caso de ser True, 
            en caso de ser False, el componente se asume como footer
        Returns:
            Componente de Dash header o footer
        """
        #______________________________________________________
        borde_h = 'var(--bs-card-inner-border-radius) var(--bs-card-inner-border-radius) 0 0'
        border_f = '0 0 var(--bs-card-inner-border-radius) var(--bs-card-inner-border-radius)'
        border =  borde_h if type_header else border_f
        #______________________________________________________
        style_comp = {
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'width': '100%',
            'height': '100%',
            'padding': '8px 12px',
            'gap':'5px',
            'border-radius':border,
            }
        style_comp.update(style)
        #______________________________________________________
        layout =  [] if layout is None else layout
        #______________________________________________________
        title =  html.Div(
            children=layout,
            style=style_comp
        )
        return title
    def card(
            self,
            header_layout=None,
            header_style={},
            body_layout=None,
            body_style={},
            footer_layout=None,
            footer_style={},
            card_style={},
            ):
        """
        Metodo para la creación la card
        Args:
            header_layout: Componente de dash la cual se insertará en el encabezado
            header_style: Estilos para el encabezado
            body_layout: Componente de dash la cual se insertará en el cuerpo
            body_style: Estilos para el cuerpo
            footer_layout: Componente de dash la cual se insertará en el footer
            footer_style: Estilos para el footer
            card_style: Estilos para el componente completo
        Returns:
            Componente de Dash con la card y actualiza el layout de la clase
        """
        ls_card = []
        #_____________________________________________________
        if header_layout is not None:
            header =self._titles(layout=header_layout,style=header_style,type_header=True) 
            header = dbc.CardHeader(
                children= header,
                style={'padding':'0px'},
                )
            ls_card = ls_card+[header]
        #_____________________________________________________
        if body_layout is not None:
            body_layout = dbc.CardBody(
                children=body_layout,
                style=body_style
                )
            ls_card=ls_card+[body_layout]
        #_____________________________________________________
        if footer_layout is not None:
            footer = self._titles(layout=footer_layout,style=footer_style,type_header=False) 
            footer = dbc.CardFooter(
                    children= footer,
                    style={'padding':'0px'},
                )
            ls_card=ls_card+[footer]
        #_____________________________________________________
        card = dbc.Card(
            children=ls_card,
            style=card_style,
            )
        self.update_layout(card)
        return card
#___________________________________________________________________________________________
