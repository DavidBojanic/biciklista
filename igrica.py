import risar
import random
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist


igra = True
sve_ovire = []
MOVEMENT = 1.4
health = 3
poeni = 0
nagrade = [("flowers.png", 1), ("bottle.png", 1), ("stones.png", 2), ("grass.png", 3), ("walker.png", 4),
           ("scooter.png", 2)]
materijalizovane_nagrade = []
gusle = "arcade.wav"
dizalica = "jump.wav"
umrlica = "explosion.wav"


class Ovira:
    def __init__(self):
        self.visina = 25
        rendi = random.randint(30, 80)
        self.sirina = rendi
        self.vrh0 = 0
        self.vrh1 = self.vrh0 + self.visina
        self.x0 = random.randint(0, risar.maxx - self.sirina)
        self.nacrtaj()
        self.collided = False

    def nacrtaj(self):
        self.body = risar.pravokotnik(self.x0, self.vrh0, self.x0 + self.sirina, self.vrh1, barva=risar.rdeca, poln=True, zaobljen=3)

    def pomjeri(self):
        self.vrh0 += 1
        self.vrh1 += 1
        self.body.setPos(self.x0, self.vrh0)

    def obrisi(self):
        risar.odstrani(self.body)


class Kolesar:
    def __init__(self):
        self.x0 = risar.maxX / 2 - 20
        self.y0 = risar.maxY - 140
        self.bodyK = risar.slika(self.x0, self.y0, "Kolesar.png")
        self.sirina = self.bodyK.boundingRect().width()
        self.visina = self.bodyK.boundingRect().height()
        self.x1, self.y1 = self.x0 + self.sirina, self.y0 + self.visina
        self.slika = "Kolesar.png"

    def lijevo(self):
        self.x0 -= MOVEMENT
        self.x1 -= MOVEMENT
        self.bodyK.setPos(self.x0, self.y0)

    def desno(self):
        self.x0 += MOVEMENT
        self.x1 += MOVEMENT
        self.bodyK.setPos(self.x0, self.y0)


class Nagrada:
    def __init__(self):
        nagrada = random.choice(nagrade)
        self.slika, self.poeni = nagrada
        self.x0 = random.randint(0, risar.maxX - 50)
        self.y0 = 0
        self.untouched = True
        self.bodyN = risar.slika(self.x0, self.y0, self.slika)
        self.sirina = self.bodyN.boundingRect().width()
        self.visina = self.bodyN.boundingRect().height()

    def pada(self):
        self.y0 += 1
        self.bodyN.setPos(self.x0, self.y0)

    def obrisi(self):
        risar.odstrani(self.bodyN)


class Gusle:
    def __init__(self):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        url = QUrl.fromLocalFile(gusle)
        self.playlist.addMedia(QMediaContent(url))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

    def play_gusle(self):

        self.player.setPlaylist(self.playlist)
        self.player.play()

    def ugasi_gusle(self):
        self.player.setMuted(True)


class Umrlica:
    def __init__(self):
        self.player = QMediaPlayer()

    def play_umrlicu(self):
        url = QUrl.fromLocalFile(umrlica)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()


class Dizalica:
    def __init__(self):
        self.player = QMediaPlayer()

    def play_dizalicu(self):
        url = QUrl.fromLocalFile(dizalica)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()


health_status = risar.besedilo(7 * risar.maxX / 10, 30, "Health : " + str(health), velikost=25)
points_status = risar.besedilo(1 * risar.maxX / 10, 30, "Points : " + str(poeni), velikost=25)
biker = Kolesar()
audio = Gusle()
audio.play_gusle()
audioD = Dizalica()
audioU = Umrlica()


def collision():
    if ((biker.y0 < ovira.vrh1 - 10 < biker.y1) or (biker.y0 < ovira.vrh0 + 10 < biker.y1)) and \
                (ovira.x0 < biker.x0 + 10 < ovira.x0 + ovira.sirina or ovira.x0 < biker.x1 - 10 < ovira.x0 + ovira.sirina):
        return True
    return False


while igra:
    if len(sve_ovire) < 20 and random.random() < 0.02:
        ovira = Ovira()
        sve_ovire.append(ovira)

    if len(materijalizovane_nagrade) < 10 and random.random() < 0.01:
        nagrada = Nagrada()
        materijalizovane_nagrade.append(nagrada)

    for n in materijalizovane_nagrade:
        n.pada()
        if (biker.y0 < n.y0 < biker.y1 or biker.y0 < n.y0 + n.visina < biker.y1) and (n.x0 < biker.x0 < n.x0 + n.sirina or n.x0 < biker.x1 < n.x0 + n.sirina):
            poeni += n.poeni
            audioD.play_dizalicu()
            points_status.setPlainText("Points: " + str(poeni))
            n.obrisi()
            materijalizovane_nagrade.remove(n)
        if n.y0 >= risar.maxy:
            n.obrisi()
            materijalizovane_nagrade.remove(n)

    for ovira in sve_ovire:
        ovira.pomjeri()

    for ovira in sve_ovire:
        if collision() and not ovira.collided:
            health -= 1
            audioU.play_umrlicu()
            if health > 0:
                health_status.setPlainText("Health: " + str(health))
                ovira.obrisi()
                sve_ovire.remove(ovira)
            if health <= 0:
                igra = False
                health_status.setPlainText("Health: 0")
                audio.ugasi_gusle()
            ovira.collided = True
        if ovira.vrh0 >= risar.maxy:
            ovira.obrisi()
            sve_ovire.remove(ovira)

    if risar.levo() and biker.x0 > MOVEMENT:
        biker.lijevo()
    if risar.desno() and biker.x0 < risar.maxx - MOVEMENT - 20:
        biker.desno()

    risar.cakaj(0.002)
risar.stoj()
