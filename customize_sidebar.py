# -*- mode: Python ; coding: utf-8 -*-

"""Anki2.1 add-on: customize sidebar of the browser."""

from aqt import mw
from aqt.browser import Browser
from aqt.qt import QIcon
from anki import version
from anki.hooks import wrap
from anki.lang import _
from operator import itemgetter

__version__ = "2.0.0"

config = mw.addonManager.getConfig(__name__)
#print("config is", config)

# check anki version. v2.1.17 has new API
anki_api_since_2_1_17 = tuple(int(i) for i in version.split(".")) >= (2,1,17)
#print("version is", version)

if anki_api_since_2_1_17:
    from aqt.browser import SidebarItem

icon_deck = ":/icons/deck.svg"
icon_tag = ":/icons/tag.svg"
icon_notetype = ":/icons/notetype.svg"
icon_heart = ":/icons/heart.svg"

#########################################
# show some items
#########################################
def custom_stdTree_until_2_1_17(self, root):
    if config['show_item_marked']:
        item = self.CallbackItem(root, _("Marked"), self._filterFunc("tag:marked"))
        item.setIcon(0, QIcon(icon_tag))
    if config['show_item_suspended']:
        item = self.CallbackItem(root, _("Suspended"), self._filterFunc("is:suspended"))
        item.setIcon(0, QIcon(icon_tag))
    if config['show_item_leech']:
        item = self.CallbackItem(root, _("Leech"), self._filterFunc("tag:leech"))
        item.setIcon(0, QIcon(icon_tag))
    if config['show_tree_today']:
        today = self.CallbackItem(root, _("Today"), None)
        today.setIcon(0, QIcon(icon_tag))
        today.setExpanded(False)
        item = self.CallbackItem(today, _("Added Today"), self._filterFunc("added:1"))
        item = self.CallbackItem(today, _("Studied Today"), self._filterFunc("rated:1"))
        item = self.CallbackItem(today, _("Again Today"), self._filterFunc("rated:1:1"))
    if config['show_tree_flags']:
        flags = self.CallbackItem(root, _("Flags"), None)
        flags.setIcon(0, QIcon(icon_tag))
        flags.setExpanded(False)
        item = self.CallbackItem(flags, _("Red"), self._filterFunc("flag:1"))
        item = self.CallbackItem(flags, _("Orange"), self._filterFunc("flag:2"))
        item = self.CallbackItem(flags, _("Green"), self._filterFunc("flag:3"))
        item = self.CallbackItem(flags, _("Blue"), self._filterFunc("flag:4"))
        item = self.CallbackItem(flags, _("No"), self._filterFunc("flag:0"))
        item = self.CallbackItem(flags, _("Any"), self._filterFunc("-flag:0"))

def custom_stdTree_since_2_1_17(self, root):
    if config['show_item_marked']:
        item = SidebarItem(_("Marked"), icon_tag, self._filterFunc("tag:marked"))
        root.addChild(item)
    if config['show_item_suspended']:
        item = SidebarItem(_("Suspended"), icon_tag, self._filterFunc("is:suspended"))
        root.addChild(item)
    if config['show_item_leech']:
        item = SidebarItem(_("Leech"), icon_tag, self._filterFunc("tag:leech"))
        root.addChild(item)
    if config['show_tree_today']:
        today = SidebarItem(_("Today"), icon_tag)
        item = SidebarItem(_("Added Today"), "", self._filterFunc("added:1"))
        today.addChild(item)
        item = SidebarItem(_("Studied Today"), "", self._filterFunc("rated:1"))
        today.addChild(item)
        item = SidebarItem(_("Again Today"), "", self._filterFunc("rated:1:1"))
        today.addChild(item)
        root.addChild(today)
    if config['show_tree_flags']:
        flags = SidebarItem(_("Flags"), icon_tag)
        item = SidebarItem(_("Red"), "", self._filterFunc("flag:1"))
        flags.addChild(item)
        item = SidebarItem(_("Orange"), "", self._filterFunc("flag:2"))
        flags.addChild(item)
        item = SidebarItem(_("Green"), "", self._filterFunc("flag:3"))
        flags.addChild(item)
        item = SidebarItem(_("Blue"), "", self._filterFunc("flag:4"))
        flags.addChild(item)
        item = SidebarItem(_("No"), "", self._filterFunc("flag:0"))
        flags.addChild(item)
        item = SidebarItem(_("Any"), "", self._filterFunc("-flag:0"))
        flags.addChild(item)
        root.addChild(flags)

if config['show_item_marked'] or \
   config['show_item_suspended'] or \
   config['show_item_leech'] or \
   config['show_tree_today'] or \
   config['show_tree_flags']:
    if anki_api_since_2_1_17:
        Browser._stdTree = wrap(Browser._stdTree, custom_stdTree_since_2_1_17)
    else:
        Browser._stdTree = wrap(Browser._stdTree, custom_stdTree_until_2_1_17)

#########################################
# collapse 'Note Types'
#########################################
def custom_modelTree_until_2_1_17(self, root, _old):
    root = self.CallbackItem(root, _("Note Types"), None)
    root.setExpanded(False)
    root.setIcon(0, QIcon(icon_notetype))
    for m in sorted(self.col.models.all(), key=itemgetter("name")):
        mitem = self.CallbackItem(
            root, m['name'], lambda m=m: self.setFilter("note", str(m['name'])))
        mitem.setIcon(0, QIcon(icon_notetype))

def custom_modelTree_since_2_1_17(self, root, _old):
    types = SidebarItem(_("Note Types"), icon_notetype)
    for m in sorted(self.col.models.all(), key=itemgetter("name")):
        item = SidebarItem(
            m["name"],
            icon_notetype,
            lambda m=m: self.setFilter("note", m["name"]),  # type: ignore
        )
        types.addChild(item)
    root.addChild(types)

if config['collapse_note_types']:
    if anki_api_since_2_1_17:
        Browser._modelTree = wrap(
            Browser._modelTree, custom_modelTree_since_2_1_17, 'around')
    else:
        Browser._modelTree = wrap(
            Browser._modelTree, custom_modelTree_until_2_1_17, 'around')

#########################################
# collapse 'Filters'
#########################################
def custom_favTree_until_2_1_17(self, root, _old):
    root = self.CallbackItem(root, _("My Filters"), None)
    root.setExpanded(False)
    root.setIcon(0, QIcon(icon_heart))
    saved = self.col.conf.get('savedFilters', {})
    for name, filt in sorted(saved.items()):
        item = self.CallbackItem(root, name, lambda s=filt: self.setFilter(s))
        item.setIcon(0, QIcon(icon_heart))

def custom_favTree_since_2_1_17(self, root, _old):
    favs = SidebarItem(_("My Filters"), icon_heart)
    for name, filt in sorted(self.col.conf.get('savedFilters', {}).items()):
        item = SidebarItem(name, icon_heart, lambda s=filt: self.setFilter(s))
        favs.addChild(item)
    root.addChild(favs)

if config['collapse_filters']:
    if anki_api_since_2_1_17:
        Browser._favTree = wrap(Browser._favTree, custom_favTree_since_2_1_17, 'around')
    else:
        Browser._favTree = wrap(Browser._favTree, custom_favTree_until_2_1_17, 'around')

#########################################
# collapse 'Decks'
#########################################
def custom_decksTree_until_2_1_17(self, root, _old):
    for i in range(root.topLevelItemCount()):
        # return item of type QTreeWidgetItem
        item = root.topLevelItem(i)
        #print("item text is '%s'" % (item.text(0)))
    root = self.CallbackItem(root, _("Decks"), None)
    root.setExpanded(False)
    root.setIcon(0, QIcon(icon_deck))
    grps = self.col.sched.deckDueTree()
    def fillGroups(root, grps, head=""):
        for g in grps:
            item = self.CallbackItem(
                root, g[0],
                lambda g=g: self.setFilter("deck", head+g[0]),
                lambda g=g: self.mw.col.decks.collapseBrowser(g[1]),
                not self.mw.col.decks.get(g[1]).get('browserCollapsed', False))
            item.setIcon(0, QIcon(icon_deck))
            newhead = head + g[0]+"::"
            fillGroups(item, g[5], newhead)
    fillGroups(root, grps)

def custom_decksTree_since_2_1_17(self, root, _old):
    decks = SidebarItem(_("Decks"), icon_deck)
    grps = self.col.sched.deckDueTree()
    def fillGroups(root, grps, head=""):
        for g in grps:
            item = SidebarItem(
                g[0],
                icon_deck,
                lambda g=g: self.setFilter("deck", head + g[0]),
                lambda expanded, g=g: self.mw.col.decks.collapseBrowser(g[1]),
                not self.mw.col.decks.get(g[1]).get("browserCollapsed", False),
            )
            root.addChild(item)
            newhead = head + g[0] + "::"
            fillGroups(item, g[5], newhead)
    fillGroups(decks, grps)
    root.addChild(decks)

if config['collapse_decks']:
    if anki_api_since_2_1_17:
        Browser._decksTree = wrap(Browser._decksTree, custom_decksTree_since_2_1_17, 'around')
    else:
        Browser._decksTree = wrap(Browser._decksTree, custom_decksTree_until_2_1_17, 'around')
