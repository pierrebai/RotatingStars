from ..animator import animator
from . import qt_drawings

from PyQt5.QtGui import QPainter, QTransform
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import QMarginsF, QRectF, Qt

class base_scene_animator(animator):
    """
    Base class for animator using Qt graphics scene and graphics items.
    """

    def __init__(self, star, options, *args, **kwargs):
        super(base_scene_animator, self).__init__(star, options, *args, **kwargs)

        self.scene = QGraphicsScene()
        self._prepare_view()

    def widget(self):
        return self.view

    def _prepare_view(self):
        self.view = QGraphicsView(self.scene)
        self.view.setInteractive(False)
        self.view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

    def reallocate_scene(self):
        self.scene = QGraphicsScene()

        self.view.setScene(self.scene)
        self.view.resetTransform()
        self.view.resetCachedContent()
        self.view.setSceneRect(QRectF())

        self.view.fitInView(self.scene.sceneRect().marginsAdded(QMarginsF(10, 10, 10, 10)), Qt.KeepAspectRatio)
        
    def adjust_view_to_fit(self):
        viewOrigin = self.view.rect().topLeft()
        sceneOrigin = self.view.mapFromScene(self.scene.sceneRect().translated(-15, -15).topLeft())
        if viewOrigin.x() >= sceneOrigin.x() or viewOrigin.y() >= sceneOrigin.y():
            #self.view.fitInView(QRectF(0, 0, 50, 50).united(self.scene.sceneRect().marginsAdded(QMarginsF(100, 100, 100, 100))), Qt.KeepAspectRatio)
            self.view.fitInView(self.scene.sceneRect().marginsAdded(QMarginsF(50, 50, 50, 50)), Qt.KeepAspectRatio)


    #################################################################
    #
    # Animator base class function overrides

    def reset(self):
        self.reallocate_scene()

