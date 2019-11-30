# -*- mode: Python ; coding: utf-8 -*-

"""Anki2.1 add-on: customize sidebar of the browser."""

from aqt import mw
from aqt.browser import Browser
from aqt.qt import QIcon
from anki.hooks import wrap
from operator import itemgetter

__version__ = "1.2.0"

config = mw.addonManager.getConfig(__name__)
#print("config is", config)

#########################################
# show some items
#########################################
def my_stdTree(self, root):
    if config['show_item_marked']:
        item = self.CallbackItem(root, _("Marked"), self._filterFunc("tag:marked"))
        item.setIcon(0, QIcon(":/icons/tag.svg"))
    if config['show_item_suspended']:
        item = self.CallbackItem(root, _("Suspended"), self._filterFunc("is:suspended"))
        item.setIcon(0, QIcon(":/icons/heart.svg"))
    if config['show_item_leech']:
        item = self.CallbackItem(root, _("Leech"), self._filterFunc("tag:leech"))
        item.setIcon(0, QIcon(":/icons/tag.svg"))
    if config['show_tree_today']:
        today = self.CallbackItem(root, _("Today"), None)
        today.setIcon(0, QIcon(":/icons/tag.svg"))
        today.setExpanded(False)
        item = self.CallbackItem(today, _("Added Today"), self._filterFunc("added:1"))
        item = self.CallbackItem(today, _("Studied Today"), self._filterFunc("rated:1"))
        item = self.CallbackItem(today, _("Again Today"), self._filterFunc("rated:1:1"))
    if config['show_tree_flags']:
        flags = self.CallbackItem(root, _("Flags"), None)
        flags.setIcon(0, QIcon(":/icons/tag.svg"))
        flags.setExpanded(False)
        item = self.CallbackItem(flags, _("Red"), self._filterFunc("flag:1"))
        item = self.CallbackItem(flags, _("Orange"), self._filterFunc("flag:2"))
        item = self.CallbackItem(flags, _("Green"), self._filterFunc("flag:3"))
        item = self.CallbackItem(flags, _("Blue"), self._filterFunc("flag:4"))
        item = self.CallbackItem(flags, _("No"), self._filterFunc("flag:0"))
        item = self.CallbackItem(flags, _("Any"), self._filterFunc("-flag:0"))

if config['show_item_marked'] or \
   config['show_item_suspended'] or \
   config['show_item_leech'] or \
   config['show_tree_today'] or \
   config['show_tree_flags']:
    Browser._stdTree = wrap(Browser._stdTree, my_stdTree)

#########################################
# collapse 'Note Types'
#########################################
def my_modelTree(self, root, _old):
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
    root = self.CallbackItem(root, _("My Filters"), None)
    root.setExpanded(False)
    root.setIcon(0, QIcon(":/icons/heart.svg"))
    saved = self.col.conf.get('savedFilters', {})
    for name, filt in sorted(saved.items()):
        item = self.CallbackItem(root, name, lambda s=filt: self.setFilter(s))
        item.setIcon(0, QIcon(":/icons/heart.svg"))

if config['collapse_filters']:
    Browser._favTree = wrap(Browser._favTree, my_favTree, 'around')

#########################################
# collapse 'Decks'
#########################################
def my_decksTree(self, root, _old):
    for i in range(root.topLevelItemCount()):
        # return item of type QTreeWidgetItem
        item = root.topLevelItem(i)
        #print("item text is '%s'" % (item.text(0)))
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
