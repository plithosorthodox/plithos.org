"""Read a SWORD zText module.

The Syriac Peshitta of 1905 is published as a SWORD module and nowhere else in
a form that can be read by machine. The format is three files to a testament:
an index of verses, an index of blocks, and the blocks themselves, deflated.
Nothing here is specific to Syriac; it will read any zText module.
"""

import struct
import zipfile
import zlib


class ZText(object):
    def __init__(self, zip_path, module):
        self.z = zipfile.ZipFile(zip_path)
        self.base = "modules/texts/ztext/%s/" % module

    def _read(self, name):
        return self.z.read(self.base + name)

    def testament(self, t, canon):
        """One testament, {book_index: {chapter: {verse: text}}}.

        `canon` is the module's versification for this testament: a list of
        books, each a list giving the number of verses in each chapter. The
        index runs testament, then for every book its own record, then for
        every chapter its record and then its verses, in that order, so a
        verse is found by counting.
        """
        bzv = self._read("%s.bzv" % t)
        bzs = self._read("%s.bzs" % t)
        bzz = self._read("%s.bzz" % t)
        blocks = {}

        def block(n):
            if n not in blocks:
                off, clen, _ulen = struct.unpack_from("<III", bzs, n * 12)
                blocks[n] = zlib.decompress(bzz[off:off + clen])
            return blocks[n]

        out = {}
        i = 1                                    # past the testament's record
        for b, chapters in enumerate(canon, 1):
            i += 1                               # past the book's record
            book = {}
            for c, nverses in enumerate(chapters, 1):
                i += 1                           # past the chapter's record
                verses = {}
                for v in range(1, nverses + 1):
                    n, start, size = struct.unpack_from("<IIH", bzv, i * 10)
                    i += 1
                    if not size:
                        continue
                    raw = block(n)[start:start + size]
                    txt = raw.decode("utf-8", "replace").strip()
                    if txt:
                        verses[v] = txt
                if verses:
                    book[c] = verses
            if book:
                out[b] = book
        return out
