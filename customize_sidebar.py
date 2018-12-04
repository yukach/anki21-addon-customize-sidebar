# -*- mode: Python ; coding: utf-8 -*-

"""
Anki2.1 add-on: customize sidebar of the browser.
"""

from aqt import mw
from aqt.browser import Browser
from aqt.qt import QIcon
from anki.hooks import wrap
#from anki.lang import ngettext
from operator import itemgetter

config = mw.addonManager.getConfig(__name__)
print("config is", config)

# see aqt/browser.py
#   def buildTree(self):
#        self.sidebarTree.clear()
#        root = self.sidebarTree
#        self._stdTree(root)
#        self._favTree(root)
#        self._decksTree(root)
#        self._modelTree(root)
#        self._userTagTree(root)
#        self.sidebarTree.setIndentation(15)

#  def _systemTagTree(self, root):
#        tags = (
#            (_("Whole Collection"), "ankibw", ""),
#            (_("Current Deck"), "deck16", "deck:current"),
#            (_("Added Today"), "view-pim-calendar.png", "added:1"),
#            (_("Studied Today"), "view-pim-calendar.png", "rated:1"),
#            (_("Again Today"), "view-pim-calendar.png", "rated:1:1"),
#            (_("New"), "plus16.png", "is:new"),
#            (_("Learning"), "stock_new_template_red.png", "is:learn"),
#            (_("Review"), "clock16.png", "is:review"),
#            (_("Due"), "clock16.png", "is:due"),
#            (_("Marked"), "star16.png", "tag:marked"),
#            (_("Suspended"), "media-playback-pause.png", "is:suspended"),
#            (_("Leech"), "emblem-important.png", "tag:leech"))
#        for name, icon, cmd in tags:
#            item = self.CallbackItem(
#                root, name, lambda c=cmd: self.setFilter(c))
#            item.setIcon(0, QIcon(":/icons/" + icon))
#        return root
#
#    def _favTree(self, root):

#    def _stdTree(self, root):
#        for name, filt, icon in [[_("Whole Collection"), "", "collection"],
#                           [_("Current Deck"), "deck:current", "deck"]]:
#            item = self.CallbackItem(
#                root, name, self._filterFunc(filt))
#            item.setIcon(0, QIcon(":/icons/{}.svg".format(icon)))


def my_stdTree(self, root):
    #root is sidebartreewidget
    for i in range(root.topLevelItemCount()):
        # return item of type QTreeWidgetItem
        item = root.topLevelItem(i)
        print("item text is '%s'" % (item.text(0)))

#    if config['show_item_marked']:
#        new_items = (
#            (_("Marked"), "tag.svg", "tag:marked"),
#            (_("Suspended"), "heart.svg", "is:suspended"))
#        for name, icon, filter_cmd in new_items:
#            item = self.CallbackItem(
#                root, name, self._filterFunc(filter_cmd))
#            item.setIcon(0, QIcon(":/icons/" + icon))
    if config['show_item_marked']:
        item = self.CallbackItem(root, _("Marked"), self._filterFunc("tag:marked"))
        item.setIcon(0, QIcon(":/icons/tag.svg"))
    if config['show_item_suspended']:
        item = self.CallbackItem(root, _("Suspended"), self._filterFunc("is:suspended"))
        item.setIcon(0, QIcon(":/icons/heart.svg"))

if config['show_item_marked']:
    Browser._stdTree = wrap(Browser._stdTree, my_stdTree)

#########################################
# collapse 'Note Types'
#########################################
def my_modelTree(self, root, _old):
    print("my_modelTree is called")
    if config['collapse_note_types']:
        # search "Note types" item
        for i in range(root.topLevelItemCount()):
            # return item of type QTreeWidgetItem
            item = root.topLevelItem(i)
            if item.text(0) == _("Note Types"):
                print("Note types item has already exists")
                return

        root = self.CallbackItem(root, _("Note Types"), None)
        root.setExpanded(False)
        root.setIcon(0, QIcon(":/icons/notetype.svg"))
        for m in sorted(self.col.models.all(), key=itemgetter("name")):
            mitem = self.CallbackItem(
                root, m['name'], lambda m=m: self.setFilter("note", str(m['name'])))
            mitem.setIcon(0, QIcon(":/icons/notetype.svg"))

if config['collapse_note_types']:
    Browser._modelTree = wrap(Browser._modelTree, my_modelTree, 'around')

#########################################
# collapse 'Filters'
#########################################
def my_favTree(self, root, _old):
    print("my_favTree is called")
    if config['collapse_filters']:
        # search "Filters" item
        for i in range(root.topLevelItemCount()):
            # return item of type QTreeWidgetItem
            item = root.topLevelItem(i)
            if item.text(0) == _("Filters"):
                print("Filters item has already exists")
                return

        root = self.CallbackItem(root, _("Filters"), None)
        root.setExpanded(False)
        root.setIcon(0, QIcon(":/icons/heart.svg"))
        saved = self.col.conf.get('savedFilters', {})
        for name, filt in sorted(saved.items()):
            item = self.CallbackItem(root, name, lambda s=filt: self.setFilter(s))
            item.setIcon(0, QIcon(":/icons/heart.svg"))
        #for m in sorted(self.col.models.all(), key=itemgetter("name")):
        #    mitem = self.CallbackItem(
        #        root, m['name'], lambda m=m: self.setFilter("filter", str(m['name'])))
        #    mitem.setIcon(0, QIcon(":/icons/heart.svg"))

if config['collapse_filters']:
    Browser._favTree = wrap(Browser._favTree, my_favTree, 'around')

#########################################
# collapse 'Decks'
#########################################
def my_decksTree(self, root, _old):
    print("_decksTree is called")
    if config['collapse_decks']:
        # search "Decks" item
        for i in range(root.topLevelItemCount()):
            # return item of type QTreeWidgetItem
            item = root.topLevelItem(i)
            if item.text(0) == _("Decks"):
                print("Decks item has already exists")
                return

        root = self.CallbackItem(root, _("Decks"), None)
        root.setExpanded(False)
        root.setIcon(0, QIcon(":/icons/deck.svg"))
        grps = self.col.sched.deckDueTree()
        def fillGroups(root, grps, head=""):
            for g in grps:
                item = self.CallbackItem(
                    root, g[0],
                    lambda g=g: self.setFilter("deck", head+g[0]),
                    lambda g=g: self.mw.col.decks.collapseBrowser(g[1]),
                    not self.mw.col.decks.get(g[1]).get('browserCollapsed', False))
                item.setIcon(0, QIcon(":/icons/deck.svg"))
                newhead = head + g[0]+"::"
                fillGroups(item, g[5], newhead)
        fillGroups(root, grps)

if config['collapse_decks']:
    Browser._decksTree = wrap(Browser._decksTree, my_decksTree, 'around')
