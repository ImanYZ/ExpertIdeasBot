
import pywikibot
from pywikibot import i18n

class ExpertIdeasBot:

    # Edit summary message that should be used is placed on /i18n subdirectory.
    # The file containing these messages should have the same name as the caller
    # script (i.e. ExpertIdeasBot.py in this case)

    def run(pageTitle, newContent):
        # Set the edit summary message
        site = pywikibot.Site()
        summary = i18n.twtranslate(site, 'ExpertIdeasBot-changing')
        page = pywikibot.Page(site, pageTitle)
        # Loads the given page, does some changes, and saves it.
        text = self.load(page)
        if not text:
            pywikibot.output(u'Page %s not retrieved appropriately.' % page.title(asLink=True))
            return

        text = text + newContent

        if not self.save(text, page, summary):
            pywikibot.output(u'Page %s not saved.' % page.title(asLink=True))

    def load(self, page):
        # Load the text of the given page.
        try:
            # Load the page
            text = page.get()
        except pywikibot.NoPage:
            pywikibot.output(u"Page %s does not exist; skipping."
                             % page.title(asLink=True))
        except pywikibot.IsRedirectPage:
            pywikibot.output(u"Page %s is a redirect; skipping."
                             % page.title(asLink=True))
        else:
            return text
        return None

    def save(self, text, page, comment=None, minorEdit=False,
             botflag=True, watchval=True):
        # Update the given page with new text.
        # only save if something was changed
        if text != page.get():
            # Show the title of the page we're working on.
            # Highlight the title in purple.
            pywikibot.output(u"\n\n>>> \03{lightpurple}%s\03{default} <<<"
                             % page.title())
            # show what was changed
            pywikibot.showDiff(page.get(), text)
            pywikibot.output(u'Comment: %s' % comment)

            try:
                page.text = text
                # Save the page
                page.save(comment=comment or self.comment,
                          minor=minorEdit, botflag=botflag, watch=watchval)
            except pywikibot.LockedPage:
                pywikibot.output(u"Page %s is locked; skipping."
                                 % page.title(asLink=True))
            except pywikibot.EditConflict:
                pywikibot.output(
                    u'Skipping %s because of edit conflict'
                    % (page.title()))
            except pywikibot.SpamfilterError as error:
                pywikibot.output(
                    u'Cannot change %s because of spam blacklist entry %s'
                    % (page.title(), error.url))
            else:
                return True
        return False


def postCommentstoTalkpages(scholarsList):
    for scholarName, scholarPublicationList, scholarComment in scholarsList:

        text = "\n== Professor " + scholarName + "'s comment on this article ==\n"
        text += "\nProfessor " + scholarName + "has recently published the following research publications which are related to this Wikipedia article:\n"
        for i in range(len(scholarPublicationList)):
            text += "Reference " + i + ": " + scholarPublicationList[i]['name'] + " , Number of Ciations: " + scholarPublicationList[i]['citationsNumber'] + "\n"
        text += "\nProfessor " + scholarName + "has reviewed this Wikipedia page, and provided us with the following comments to improve its quality:\n"
        text += "\n" + scholarComment + "\n"
        text += "\nWe hope Wikipedians on this talk page can take advantage of these comments and improve the quality of the article accordingly.\n"
        text += "\n~~~~\n"

        bot = ExpertIdeasBot()
        bot.run("Talk:" + articleTitle, text)
        # Add the main article to my watchlist to be informed about the Wikipedians' reactions to the comment.
        bot.run(articleTitle, "")
