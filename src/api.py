
import base64
import calendar
from datetime import datetime
from io import BytesIO
from PIL import ImageTk, Image, ImageFont, ImageDraw
import requests
import os.path as path_os, os
import subprocess as subp
import zipfile
import csv, json
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base as sql_declarative_base
from sqlalchemy.orm import sessionmaker as sql_sessionmaker
import hashlib, websocket
from requests.exceptions import HTTPError, RequestException
from jinja2 import Template as JTemplate
from typing import Callable, Literal, Any, Type
import tkinter as tk
import tkinter.ttk as ttk
import win32gui, win32con, win32api, win32ui, uuid
import win32file
from io import TextIOWrapper
import vlc
import yaml
import random
from src.dlls import LIBPNG16_16DLL
from src.icons import (
	ICO_ATTENTION,
	ICO_BACKUP,
	ICO_BACKWARD,
	ICO_FORWARD,
    ICO_INFO,
    ICO_NEW,
    ICO_PAUSE,
    ICO_PLAY,
    ICO_REFRESH,
    ICO_RUN,
    ICO_SEARCH,
    ICO_STOP,
    ICO_TAKE_THUMBNAIL,
    ICO_TRASH,
    ICO_UPNDOWN,
    ICO_WARN,
    IMG_LOGO,
    IMG_WELCOME
)
"""
All of the LPRT API / Utility Functions to build your own extension!

API Function Names are written in PascalCase, so the user will not confuse with internal functions!
The internal function names are written in snake_case, like its should be!
"""

class Errors:
    USER_INPUT_NOT_IN_RANGE = 0
    FILE_ALREADY_EXISTS = 1
    OPTION_DOES_NOT_EXIST = 2
    FILE_DOES_NOT_EXIST = 3
    OBS_AUTH_FAILED = 4
    OBS_CONNECTION_BREAKUP = 5
    OBS_CORRUPTED_DATA = 6
    FFMPEG_NOT_INSTALLED = 7
    FFMPLAY_NOT_INSTALLED = 8
    WRONG_FILE_FORMAT = 9
    NO_FILE_SELECTED = 10
    FFMPEG_FILE_CREATION_ERROR = 11

LOG_DEBUG = 0
LOG_INFO = 1
LOG_WARNING = 2
LOG_ERROR = 3

USERNAME = os.getlogin()

COPYRIGHT = f"LPRT <VERSION_STR_MISSING> - <HASH_STR_MISSING> | GPL 3.0 - (c) Justus Decker 2024 - 2026"

DISCLAIMER = f"""
{COPYRIGHT}
Welcome to LPRT

A Let's Play automation tool that simplifies your workflow 
for recording, editing, and distribution.

Do you find a bug? Share it with us!

For Documentation, please look up the GitHub-wiki
"""[1:-1]

ROOT = f'C:\\Users\\{USERNAME}\\lprt\\'

__LICENSE__ = """
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:

    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an "about box".

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<https://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<https://www.gnu.org/licenses/why-not-lgpl.html>.
"""

TK_PACK = 'Pack'
TK_GRID = 'Grid'
FFMPEG_DEFAULT = ['ffmpeg', '-v', 'quiet', '-stats' , '-loglevel', 'error', '-y']

FFMPEG_GET_FRAME = [*FFMPEG_DEFAULT, '-ss', '{{time}}' , '-accurate_seek', '-i', '{{input_filepath}}', '-frames:v', '1', '{{output_filepath}}']

FFMPEG_GET_LENGTH = ['ffprobe', '-v', 'error', '-select_streams', 'v:0','-show_entries', 'stream=duration', '-of', 'default=noprint_wrappers=1:nokey=1', '{{input_filepath}}']

type GenericMenu = dict[str, str | list[dict[str, str | Callable[[], None]]]]

def AddView(view: ttk.Widget):
    TkinterApp.pages.append((view, view.NAME))

def AddMenu(data: GenericMenu): 
    """
    Add your custom Menus by calling this function with:
    {
        'name': 'Pages',
        'entrys': [
            {'label': 'Recording', 'command': lambda: print('Recording')},
            {'label': 'FetchAudio', 'command': lambda: print('FetchAudio')}
        ]
    }
    """
    TkinterApp.sub_menus.append(data)

def B64ToImage(var: str) -> ImageTk.PhotoImage:
    #! Optimize RAM Usage by using Image Maps - Global var
    decoded_data =  base64.b64decode(var.encode('ascii'))
    io_stream = BytesIO(decoded_data)
    img = Image.open(io_stream)
    return ImageTk.PhotoImage(img)

def DownloadFile(url: str, filepath: str) -> str | Literal[True]:
    try:
        r = requests.get(url)
        r.raise_for_status()

        with open(filepath, 'wb') as file:
            file.write(r.content)
        return True
    except (HTTPError, RequestException) as E:
        return str(E)
    
def DownloadAndUnzipFfmpeg():
    url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
    
    result = DownloadFile(url,'ffmpeg.zip')
    if result is not True:
        MessageBox('Cannot download file',
            f'Statuscode: {result}',
            MSGBoxPresets.SYSTEM_ALERT,
            MsgBoxFlags.SoundFlags.ERROR
            )
        return
    
    zip = zipfile.ZipFile('ffmpeg.zip')
    for ext in ['ffmpeg.exe','ffprobe.exe','ffplay.exe']:
        with open(ext,'wb') as f:
            f.write(zip.read(f'{zip.infolist()[0].filename}bin/{ext}'))

def RenderTemplate(text: str, **replacers):
    return JTemplate(text).render(**replacers)

def FfmpegBuildCommand(cmd: list[str], replacer: dict[str,str]):
    cmd_length = len(cmd)
    new_cmd = []
    print(replacer)
    for i in range(cmd_length):
        old = cmd[i]
        new_cmd.append(old)
        for key in replacer:
            print(key)
            new = RenderTemplate(old, **{key: replacer[key]})
            if new != old and (new and old):
                print(f'[{old}] [{new}] -> {key}')
                new_cmd[-1] = new
                break
    return new_cmd
       
def FfmpegRunCommand(cmd: list[str], replacer: dict[str,str]={},get_output: bool = False):
    if get_output:
        return subp.run(
            FfmpegBuildCommand(cmd,replacer), 
            subp.CREATE_NO_WINDOW, 
            capture_output=True, 
            text=True,
            shell= True).stdout
    else:
        try:
            subp.run(
                FfmpegBuildCommand(cmd,replacer), 
                subp.CREATE_NO_WINDOW,
                shell= True
                )
            return True
        except FileNotFoundError:
            return None
        
def TryDeleteFile(filepath: str | None) -> bool:
    if filepath is not None:
        if path_os.isfile(filepath):
            os.remove(filepath)
            return True
    return False

def RemoveIfExist(filepath: str) -> None:
    if path_os.isfile(filepath):
        os.remove(filepath)

def FileRead(filepath : str) -> str:
    with open(filepath, 'r') as f:
        return f.read()

def FileWrite(filepath : str, data : str):
    """ This function overwrites the file if it already exists. """
    with open(filepath, 'w') as f:
        f.write(data)
        
def FileAppend(filepath : str, data : str):
    """ If the file does not exist, it will be created. """
    with open(filepath, 'a') as f:
        f.write(data)

def CSVWrite(filepath: str, data: list[Any]):
    """ This function overwrites the file if it already exists. """
    with open(filepath,'w',newline="") as f:
              
        w = csv.writer(f,delimiter='|',)
        w.writerows(data)

def CSVRead(filepath: str) -> list[list[str]]:
    with open(filepath,'r',newline="") as f: 
        w = csv.reader(f,delimiter='|',)
        return [row for row in w]

def JSONRead(filepath : str) -> dict | list:
    with open(filepath, 'r') as f:
        return json.load(f)
    
def JSONWrite(filepath : str, data : dict | list):
    """ This function overwrites the file if it already exists. """
    with open(filepath, 'w') as f:
        f.write(json.dumps(data))

def CreateFullPathIfNotExist(path: str):
    """
    Checks if a directory path exists, and if not, creates all necessary
    intermediate directories to ensure the full path exists.

    This function iterates through the components of the given path and
    creates each subdirectory if it doesn't already exist, effectively
    creating a nested directory structure.
    """
    if not path_os.isdir(path):
        sp = path.split('\\')
        for idx in range(len(sp)):
            if not idx: continue
            cp = "\\".join(sp[0:idx+1]) + '\\'
            if not path_os.isdir(cp):
                os.mkdir(cp)
   
def Log(message: str, 
        *variables: Any, 
        logtype: Literal[0] | Literal[1] | Literal[2] | Literal[3] = 0): 
    TYPES = [int, str, bool, float, dict, tuple, list, bytes]
    LOG_TYPES = ('DEB','INF','WAR','ERR')
    LOG_COLORS = ('\033[34;1;1m','\033[32;1;1m','\033[33;1;1m','\033[31;1;1m')
    
    VALUE_COLORS = [
            '#CCFF99',
            '#FFCC99',
            '#FF9999',
            '#99FFFF',
            '#FFFF99',
            '#FF99FF',
            '#9999FF',
            '#FF99CC',
            '#FFCC00'
        ]
    
    
    logtype_str = LOG_TYPES[logtype]
    logcolor = LOG_COLORS[logtype]
    output = ''
    var_step = 0
    
    def _hex_to_rgb(hex: str) -> tuple[int, ...]:
        return tuple(int(hex[1:][i:i+2], 16) for i in (0, 2, 4))
    
    def _colorize_text(col: str, text: str):
        r, g, b = _hex_to_rgb(col)
        return f'\033[38;2;{r};{g};{b}m{text}\033[0m'

    if not variables:
        print(f'[{logcolor}{logtype_str}\033[0m] {message}\033[0m')
        return

    for word in message:
        if word == '$' and var_step <= len(variables) - 1:
            color_picker = 2
            if variables[var_step] is not None:
                color_picker = [isinstance(variables[var_step], typ) for typ in TYPES].index(True)

            if color_picker == 1 and variables[var_step].startswith('#') and variables[var_step].__len__() == 7:
                # Is a Hex Color Value
                word = _colorize_text(variables[var_step],variables[var_step])
            else:
                word = _colorize_text(VALUE_COLORS[color_picker],variables[var_step])
            var_step += 1
        elif var_step > len(variables) - 1 and word == '$':
            word = '[NULL]'
        
        output += word
        
    print(f'[{logcolor}{logtype_str}\033[0m] {output}\033[0m')
    
def DisableWidgets(*objs: ttk.Widget):
    for obj in objs:
        obj.state(["disabled"])

def EnableWidgets(*objs: ttk.Widget):
    for obj in objs:
        obj.state(["!disabled"])
        
def TkinterWidgetBuilder(obj: ttk.Widget, 
                         obj_kwargs: dict[str, Any],
                         package_method: Literal['Grid'] | Literal['Pack'], 
                         package_options: dict[str, str | int] | None = None,
                         ) -> ttk.Widget:
    if package_options is None: package_options = {}
    _new_instance = obj(**obj_kwargs)
    if package_method == TK_PACK:
        _new_instance.pack(**package_options)
    elif package_method == TK_GRID:
        _new_instance.grid(**package_options)
    else:
        raise TypeError
    return _new_instance

class AutomationError(Exception):
	"""
	If this error is thrown. The user has done some bullshit, in most cases:
    The user forgot to do a earlier automation or deleted some files.
    In rare cases the programmer has done something wrong here!
    This Exception should be catched, so the user can get a simple error message,
    without throwing too much code in between the automations that makes it nearly unreadable.
 	"""

class View(ttk.Frame):
    """
    Naming-conventions:
    _ prefix -> only for labels, one time access
    normal -> for others
    """
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.mF = ttk.Frame(self)
        self.menu = parent.master
        self.mF.pack()
        
class GenericWorkFlow:
    def __init__(self, 
                 folder: str, 
                 finish_message: str, 
                 lpid: int, 
                 epr: tuple[int, int],
                 lp_name: str) -> None:
        self.auto_create_folder_path = folder
        self.finish_message = finish_message
        self.lpid,self.epr = lpid,epr
        self.lp_name = lp_name
    
    def on_workflow_start(self): 
        CreateFullPathIfNotExist(self.auto_create_folder_path)
        
    def on_workflow_progression(self): ...
    
    def on_workflow_end(self): 
        TMSG.show('Workflow finished', self.finish_message)
    
    def workflow(self): ...
    
    @property
    def rng(self) -> tuple[int,int]:
        return self.epr[0],self.epr[1]+(1 if self.epr[0] == self.epr[1] else 0)
    
class __ToastMessager:
    ERROR = win32gui.NIIF_ERROR
    INFO = win32gui.NIIF_INFO
    WARNING = win32gui.NIIF_WARNING
    """
    Instanciate this once!
    
    After that use the show method:
        It used the title, message & from the ToastIcon Class the Icon.
    """
    def __init__(self):
        self.class_name = f"LPRTToast_{uuid.uuid4().hex}"
        
        wc = win32gui.WNDCLASS()
        self.hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = self.class_name
        
        wc.lpfnWndProc = self.__wnd_proc 
        
        try:
            self.class_atom = win32gui.RegisterClass(wc)
        except Exception as e:
            print(f"Class registration failed: {e}")

    def __wnd_proc(self, hwnd, msg, wparam, lparam) -> int:
        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0  # LRESULT Success
        # Failed Messages must be send to DefWindowProc
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    
    def show(self, title: str, message: str, icon: int | None = None):
        if icon is None:
            icon = __ToastMessager.INFO
        hwnd = win32gui.CreateWindow(
            self.class_name, 
            "ToastWindow", 
            win32con.WS_OVERLAPPED,
            0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
            0, 0, self.hinst, None
        )
        
        win32gui.UpdateWindow(hwnd)
        
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
    
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO
        nid = (
            hwnd,                          # Window Handle
            0,                             # ID
            flags,                         # Configuration-Flags
            win32con.WM_USER + 20,         # Callback Message
            hicon,                         # Icon Handle
            "Python Tooltip",              # Hover-Text
            message,                       # Textcontent
            10,                            # Timeout
            title,                         # Title
            icon                           # Icon-Type (Info)
        )
        
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        
TMSG = __ToastMessager()

class MsgBoxFlags:
    class SoundFlags:
        INFORMATION = 64
        WARNING = 48
        ERROR = 16
        OK = 0

    class ReturnFlags:
        OK = 1
        CANCEL = 2
        ABORT = 3
        RETRY = 4
        IGNORE = 5
        YES = 6
        NO = 7
        TRY_AGAIN = 10
        CONTINUE = 11

    class Buttons:
        ABORT_RETRY_IGNORE = 0x00000002
        CANCEL_RETRY_CONTINUE = 0x00000006
        HELP = 0x00004000
        OK = 0x00000000
        OK_CANCEL = 0x00000001
        RETRY_CANCEL = 0x00000005
        YES_NO = 0x00000004
        YES_NO_CANCEL = 0x00000003

    class Icons:
        WARNING = 0x00000030
        INFORMATION = 0x00000040
        QUESTION = 0x00000020
        ERROR = 0x00000010
        
    class DefaultButton:
        BTN1 = 0x00000000
        BTN2 = 0x00000100
        BTN3 = 0x00000200
        BTN4 = 0x00000300

    class Modals:
        APPL = 0x00000000
        SYSTEM = 0x00001000
        TASK = 0x00002000
        
    class WindowOptions:
        DEFAULT_DESKTOP_ONLY = 0x00020000
        RIGHT = 0x00080000
        RT_LEADING = 0x00100000
        SET_FOREGROUND = 0x00010000
        TOPMOST = 0x00040000
        SERVICE_NOTIFICATION = 0x00200000

class MSGBoxPresets:
    CRITICAL_RETRY = MsgBoxFlags.Icons.ERROR | MsgBoxFlags.Buttons.ABORT_RETRY_IGNORE | MsgBoxFlags.DefaultButton.BTN2
    CONFIRM_QUESTION = MsgBoxFlags.Icons.QUESTION | MsgBoxFlags.Buttons.YES_NO | MsgBoxFlags.WindowOptions.SET_FOREGROUND
    SYSTEM_ALERT = MsgBoxFlags.Icons.WARNING | MsgBoxFlags.Buttons.OK | MsgBoxFlags.Modals.SYSTEM | MsgBoxFlags.WindowOptions.TOPMOST
    SAFE_INFO = MsgBoxFlags.Icons.INFORMATION | MsgBoxFlags.Buttons.OK_CANCEL | MsgBoxFlags.DefaultButton.BTN2

def MessageBox(title: str, msg: str, style: int = MSGBoxPresets.SAFE_INFO, snd: int = MsgBoxFlags.SoundFlags.OK):
    """
    A Wrapper for the win32ui.MessageBox

    More information for Flags here: https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messagebox
    """
    
    win32api.MessageBeep(snd)
    return win32ui.MessageBox(msg, title, style)

class OBSWSClient:
    """
    By using OBS v5 we get the current recording time etc.
    """
    def __init__(self, host="localhost", port=4455, password=""):
        self.url = f"ws://{host}:{port}"
        self.password = password
        self.ws = None
        self.msg_id = 0
    
    def __generate_auth(self, salt, challenge) -> str:
        # hash & salt
        secret_hash = hashlib.sha256((self.password + salt).encode('utf-8')).digest()
        secret_b64 = base64.b64encode(secret_hash).decode('utf-8')
        
        # Hash the result with the challenge
        auth_hash = hashlib.sha256((secret_b64 + challenge).encode('utf-8')).digest()
        auth_b64 = base64.b64encode(auth_hash).decode('utf-8')
        return auth_b64

    def connect(self)  -> str | None:
        """
        Connects to OBSWS, if any error is raised during this: we return a string(containing the Exception) else None
        """
        try:
            self.ws = websocket.create_connection(self.url)
            
            # Get hello
            
            hello = json.loads(self.ws.recv())
            print("Connection to OBS established!")
            # generate identify
            
            identify_data = {
                "op": 1, # OpCode 1: Identify
                "d": {"rpcVersion": 1,}
            }
            # send identify
            if "authentication" in hello["d"]:
                salt = hello["d"]["authentication"]["salt"]
                challenge = hello["d"]["authentication"]["challenge"]
                auth_string = self.__generate_auth(salt, challenge)
                
                identify_data["d"]["authentication"] = auth_string

            self.ws.send(json.dumps(identify_data))
            
            identified = json.loads(self.ws.recv())
            if identified["op"] == 2:
                print("Auth Success!")
        except Exception as E:
            return str(E)
    
    def GetOutputStatus(self):
        
        result = self.call("GetOutputStatus",{"outputName": 'adv_file_output'})
        if 'error' in result: 
            print(result)
            return None
        return result['d']['responseData']
    
    def GetRecordingTime(self):
        result = self.GetOutputStatus()
        if result is None: return None
        return result['outputTimecode']
        
    def call(self, request_type, request_data=None):
        """
        Sends a call / a manually Request(OpCode 6) to the WS
        """
        try:
            self.msg_id += 1
            payload = {
                "op": 6, # OpCode 6: Request
                "d": {
                    "requestType": request_type,
                    "requestId": f"req_{self.msg_id}",
                    "requestData": request_data or {}
                }
            }
            
            self.ws.send(json.dumps(payload))
            return json.loads(self.ws.recv())
        except Exception as E:
            return {'error': str(E)}
        
class AudacityPipeline:
  
    """
    This Module contains everything you need to connect to the Audacity in a safe way.

    Contains:
    - Sending Commands
    - Receiving Results from Audacity
    - Errorhandling

    How to enable the Audacity pipeline?
    Open Audacity
    Go to: Edit > Settings > Module > enable mod-script-pipe
    Reopen Audacity & Reopen LPRT(When open)
    """
    TO_NAME = '\\\\.\\pipe\\ToSrvPipe'
    FROM_NAME = '\\\\.\\pipe\\FromSrvPipe'
    
    TO_FILE: None | TextIOWrapper = None
    FROM_FILE: None | TextIOWrapper = None
	
    @staticmethod
    def create_pipe():
        """
        Establish the connection between LPRT & Audacity.
        """
        Log("Both pipes exist.  Good.",logtype=LOG_INFO)

        #AFA.TO_FILE = open(AFA.TO_NAME, 'w')
        

        AudacityPipeline.TO_FILE = win32file.CreateFile(AudacityPipeline.TO_NAME, 
                                win32file.GENERIC_WRITE,
                                win32file.FILE_SHARE_WRITE,
                                None,
                                win32file.OPEN_EXISTING,
                                win32file.FILE_ATTRIBUTE_NORMAL,
                                0)
        Log("File to write to has been opened",logtype=LOG_INFO)
        """
        On the testsystem(Windows 11) the connection to the mod-pipe will be established only:
        When The following code does its thing!
        Make sure Audacity is running!
        """
        AudacityPipeline.FROM_FILE = win32file.CreateFile(AudacityPipeline.FROM_NAME, 
                                win32file.GENERIC_READ,
                                win32file.FILE_SHARE_READ,
                                None,
                                win32file.OPEN_EXISTING,
                                win32file.FILE_ATTRIBUTE_NORMAL,
                                0)

        Log(f"Opened {AudacityPipeline.FROM_NAME}",logtype=LOG_INFO)
    @staticmethod
    def break_pipe():
        win32file.CloseHandle(AudacityPipeline.TO_FILE)
        win32file.CloseHandle(AudacityPipeline.FROM_FILE)
        AudacityPipeline.TO_FILE.close()
        AudacityPipeline.FROM_FILE.close()
        Log("Destroyed pipes & closed AFA's",logtype=LOG_INFO)
        
    @staticmethod
    def send_command(command):
        """Send a single command."""
        Log("Send: >>> \n"+command,logtype=LOG_INFO)
        while 1:
            try:
                win32file.WriteFile(AudacityPipeline.TO_FILE,str(command + '\r\n\0').encode())
                win32file.FlushFileBuffers(AudacityPipeline.TO_FILE)
                break
            except:
                pass
            
    @staticmethod
    def get_response() -> str:
        """Return the command response."""
        result = ''
        line = b''
        while True:
            result += line.decode()
            try:
                _,line = win32file.ReadFile(AudacityPipeline.FROM_FILE,-1)
                Log("ACR $ $",[_,line])
                if line == b'BatchCommand finished: OK\n\n':
                    break
            except Exception as E:
                Log("Audacity Response Error $", [str(E)], LOG_WARNING)
                break
        return result
    
    @staticmethod
    def do_command(command) -> str:
        """Send one command, and return the response."""
        response = None
        try:
            AudacityPipeline.send_command(command)
            response = AudacityPipeline.get_response()
        except Exception as E:
            Log("Audacity Error $",[str(E)])
        return response
      
class TkinterApp(tk.Tk):
    """
    The main application window for the multi-page Tkinter application.

    This class extends `tk.Tk` and provides a framework for managing
    multiple distinct pages (frames) within a single window. It initializes
    each page and allows seamless navigation between them.
    """
    pages: list[tuple[ttk.Widget, str]] = []
    sub_menus: list[GenericMenu] = []
    on_page_change_hooks: set[Callable] = set()
    
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
     
        self.title(f'LPRT')
        self.geometry('1024x768')
        
        self.MENU = tk.Menu(self)
        self.config(menu = self.MENU)
        
        self.sub_menus.insert(0, {
            'name': 'LPRT',
            'entrys': [
                {'label': 'QUIT', 'command': lambda: print('QUIT')},
                {'label': 'Settings', 'command': lambda: print('Settings')}
            ]
        })
        
        container = tk.Frame()
        
        self.__frames = {}
        
        self.ordered_frames = []
        
        for view, name in self.pages:
            frame = view(container)
            self.ordered_frames.append(view)
            self.__frames[view] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            
        self.sub_menus.insert(0, {
            'name': 'Pages',
            'entrys': [
                {'label': n.NAME, 'command': lambda n=n: self.show_frame(n)} for n in self.ordered_frames
            ]
        })
        container.pack()
        container.pack(side = "top", fill = "both", expand = True) 
 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.show_frame(self.ordered_frames[0])
        
        for sub_menu in self.sub_menus:
            name = sub_menu['name']
            _menu = tk.Menu(self.MENU, tearoff=0)
            self.MENU.add_cascade(label = name, menu = _menu)
            for entry in sub_menu['entrys']:
                _menu.add_command(**entry)
        
        #* Pages: User Automations
        #* Database related: Export, import etc.
        #* Filesystem related: Data Detection, Create Lets Play, Backup etc.
        #* Settings related
        #* About: Help, License etc.
        
        
    
        self.wm_iconphoto(False,B64ToImage(IMG_LOGO))
    
    def show_frame(self, cont: str):
        for hook in TkinterApp.on_page_change_hooks:
            Log('UpdateHookExecution: $',str(hook))
            hook()
        frame = self.__frames[cont]
        frame.tkraise()

class LPSelector(ttk.Frame):
    def __init__(self, parent, sql_hook: Callable):
        super().__init__(parent)
        self.sql_hook = sql_hook
        self.selected = tk.StringVar(self,'None')
        self.reset()
        TkinterApp.on_page_change_hooks.add(self.reset)
        
    def reset(self):
        if hasattr(self, 'self.selector'):
            self.selector.destroy()
            del self.selector
            
        if hasattr(self, 'self.label'):
            self.label.destroy()
            del self.label
            
        data = self.sql_hook()
        
        self.label = TkinterWidgetBuilder(
            ttk.Label,
            {'master': self, 'text': 'Lets Play'},
            TK_GRID,
            {'row': 0, 'column': 0}
        )
        
        self.selector = ttk.OptionMenu(
                self,
                self.selected,
                'None',
                        *data
        )

        self.selector.grid(row=0,column=1)

        self.selected.set('None')
        
    def get(self):
        v = self.selected.get()
        if not v or v == 'None':
            return None
        return v

class EPSelector(ttk.Frame):
    def __init__(self, parent, sql_hook: Callable, name: str):
        super().__init__(parent)
        self.name = name
        self.sql_hook = sql_hook
        self.selected = tk.StringVar(self, '0')
        self.reset()
        TkinterApp.on_page_change_hooks.add(self.reset)
    
    def reset(self):
        
        if hasattr(self, 'self.selector'):
            self.selector.destroy()
            del self.selector
            
        if hasattr(self, 'self.label'):
            self.label.destroy()
            del self.label
        
        length = len(self.sql_hook())
        
        self.label = TkinterWidgetBuilder(
            ttk.Label,
            {'master': self, 'text': self.name},
            TK_GRID,
            {'row': 0, 'column': 0}
        )
        
        self.selector = TkinterWidgetBuilder(
            ttk.Spinbox,
            {'master': self,'textvariable': self.selected, 'from_': 1 if length else 0, 'to': length, 'width': 5},
            TK_GRID,
            {'row': 0, 'column': 1}
        )
        
        self.selected.set(str(length))
    
    def get(self):
        v = self.selected.get()
        if not v or not v.isdecimal():
            return None
        return int(v)
    
class LPEP(ttk.Frame):
    def __init__(self, 
                 parent,
                 letsplay_hook: Callable,
                 episodes_hook: Callable,
                 run_callback: Callable):
        super().__init__(parent)
        self.run_callback = run_callback
        self.main_label = TkinterWidgetBuilder(
            ttk.LabelFrame,
            {'master': self, 'text': 'LPEP Selector'},
            TK_PACK
        )
        
        self.letsplay = TkinterWidgetBuilder(
            LPSelector,
            {'parent': self.main_label, 'sql_hook': letsplay_hook},
            TK_GRID,
            {'row': 0, 'column': 0}
        )
        
        self.start_episode = TkinterWidgetBuilder(
            EPSelector,
            {'parent': self.main_label, 'sql_hook': episodes_hook, 'name': 'start'},
            TK_GRID,
            {'row': 0, 'column': 1}
        )
        
        self.end_episode = TkinterWidgetBuilder(
            EPSelector,
            {'parent': self.main_label, 'sql_hook': episodes_hook, 'name': 'end'},
            TK_GRID,
            {'row': 0, 'column': 2}
        )
        
        self.run_button = TkinterWidgetBuilder(
            ttk.Button,
            {'master': self.main_label, 'command': self.execute_given_command},
            TK_GRID,
            {'row': 0, 'column': 3}
        )
    
    def execute_given_command(self, *_):
        lp = self.letsplay.get()
        ep1 = self.start_episode.get()
        ep2 = self.end_episode.get()
        if lp is None or ep1 is None or ep2 is None:
            MessageBox('Error', 'One or more inputs are empty', MSGBoxPresets.SYSTEM_ALERT, MsgBoxFlags.SoundFlags.ERROR)
            return
        if ep1 < 1 or ep2 < 1:
            MessageBox('Error', 'inputs are zero or less... why?', MSGBoxPresets.SYSTEM_ALERT, MsgBoxFlags.SoundFlags.ERROR)
            return
        if ep1 > ep2:
            MessageBox('Error', 'End must be greater than start', MSGBoxPresets.SYSTEM_ALERT, MsgBoxFlags.SoundFlags.ERROR)
            return
        
        self.run_callback((ep1, ep2), lp)
        
class DateEntry(ttk.Frame): 
    def __init__(self, parent):
        super().__init__(parent)
        self.main_label = TkinterWidgetBuilder(
            ttk.LabelFrame,
            {'master': self, 'text': 'DateEntry'},
            TK_PACK
        )
        
        self.month_changer = TkinterWidgetBuilder(
            ttk.Frame,
            {'master': self.main_label},
            TK_PACK
        )
        
        self.last_month = TkinterWidgetBuilder(
            ttk.Button,
            {'master': self.month_changer, 'command': self.change_to_last_month, 'width': 4, 'text': '<<'},
            TK_GRID,
            {'row': 0, 'column': 0}
        )
        
        self.this_year_and_month = TkinterWidgetBuilder(
            ttk.Label,
            {'master': self.month_changer, 'text': 'Current', 'width': 20},
            TK_GRID,
            {'row': 0, 'column': 1}
        )
        self.this_year_and_month.config(anchor='center')
        
        self.next_month = TkinterWidgetBuilder(
            ttk.Button,
            {'master': self.month_changer, 'command': self.change_to_next_month, 'width': 4, 'text': '>>'},
            TK_GRID,
            {'row': 0, 'column': 2}
        )
        
        self.calendar = TkinterWidgetBuilder(
            ttk.Frame,
            {'master': self.main_label},
            TK_PACK
        )
        
        self.current = datetime.now()
        
        
        self.buttons: list[ttk.Button] = []
        self.reset()
    @staticmethod
    def add_months(current_date: datetime, months_to_add: int):
        new_date = datetime(current_date.year + (current_date.month + months_to_add - 1) // 12,
                            (current_date.month + months_to_add - 1) % 12 + 1,
                            current_date.day, current_date.hour, current_date.minute, current_date.second)
        return new_date
        
    def change_to_next_month(self, *_):
        self.current = DateEntry.add_months(self.current, 1)
        self.reset()
        
    def change_to_last_month(self, *_):
        self.current = DateEntry.add_months(self.current, -1)
        self.reset()

    def set_date(self, d):
        print(d)
    
    def reset(self):
        
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()
        

        year, month = self.current.year, self.current.month

        self.this_year_and_month.config(text = f'{calendar.month_name[month]} - {year}')
        entrys = calendar.monthcalendar(year, month)
        
        for i, wd in enumerate(['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']):
            label = TkinterWidgetBuilder(
                ttk.Label,
                {'master': self.calendar, 'text': wd},
                TK_GRID,
                {'row': 0, 'column': i}
            )
            self.buttons.append(label)
        
        for w, week in enumerate(entrys):
            for d, day in enumerate(week):
                if day == 0: continue
                btn = TkinterWidgetBuilder(
                    ttk.Button,
                    {'master': self.calendar, 'command': lambda day=day: self.set_date(day), 'width': 2, 'text': str(day)},
                    TK_GRID,
                    {'row': w+1, 'column': d}
                )
                self.buttons.append(btn)
        
class TimeEntry(ttk.Frame): 
    def __init__(self, parent):
        super().__init__(parent)
        self.hours = tk.StringVar(self, "0")
        self.minutes = tk.StringVar(self, "0")
        
        
        self.main_label = TkinterWidgetBuilder(
            ttk.LabelFrame,
            {'master': self, 'text': 'Time Input(hh/mm): '},
            TK_PACK
        )
        
        self.hours_input = TkinterWidgetBuilder(
            ttk.Spinbox,
            {'master': self.main_label,'textvariable': self.hours, 'from_': 0, 'to': 23, 'width': 5},
            TK_GRID,
            {'row': 0, 'column': 0}
        )
        
        self.delimiter = TkinterWidgetBuilder(
            ttk.Label,
            {'master': self.main_label, 'text': ': '},
            TK_GRID,
            {'row': 0, 'column': 1}
        )
        
        self.minutes_input = TkinterWidgetBuilder(
            ttk.Spinbox,
            {'master': self.main_label,'textvariable': self.minutes, 'from_': 0, 'to': 23, 'width': 5},
            TK_GRID,
            {'row': 0, 'column': 2}
        )
        
    def get(self, _as: Type = int):
        v_h, v_m = self.hours.get(), self.minutes.get()
        
        if not v_h.isdecimal() or not v_m.isdecimal():
            return None
        
        hours, minutes = int(v_h), int(v_m)
        
        if hours > 23 or hours < 0:
            return None
        
        if minutes > 59 or minutes < 0:
            return None
    
        if _as == int:
            return (hours, minutes)
        elif _as == str:
            hours = hours if hours > 9 else f'0{hours}'
            minutes = minutes if minutes > 9 else f'0{minutes}'
            return f"{hours}:{minutes}"
        else:
            raise NotImplementedError
    
class MediaPlayer(ttk.Frame): 
    _is_playing: bool = False
    _is_loaded: bool = False
    _current_playing_instance = None
    _vlc_instance = vlc.Instance()
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.slider_dragging = False
        self.vol = 50
        
        self.__current_file = ''
        self.__player = MediaPlayer._vlc_instance.media_player_new()
        
        # b64 images
        _play = B64ToImage(ICO_PLAY)
        _stop = B64ToImage(ICO_STOP)
        _pause = B64ToImage(ICO_PAUSE)
        _forward = B64ToImage(ICO_FORWARD)
        _backward = B64ToImage(ICO_BACKWARD)
        
        self.video_view = TkinterWidgetBuilder(
            tk.Canvas,
            {'master': self, 'bg': 'black'},
            TK_PACK,
            {'fill': tk.BOTH, 'expand': True, 'padx': 2, 'pady': (2,0)}
        )
        
        self.controls = TkinterWidgetBuilder(
            ttk.Frame,
            {'master': self},
            TK_PACK
        )
        
        self.play_btn = TkinterWidgetBuilder(
            ttk.Button,
            {'master': self.controls, 'command': self.__play_video, 'image': _play},
            TK_PACK,
            {'side': tk.LEFT, 'padx': 2}
        )
        
        self.fb_btn = TkinterWidgetBuilder(
            ttk.Button,
            {'master': self.controls, 'command': self.last_media, 'image': _backward},
            TK_PACK,
            {'side': tk.LEFT, 'padx': 2}
        )
        
        self.ff_btn = TkinterWidgetBuilder(
            ttk.Button,
            {'master': self.controls, 'command': self.next_media, 'image': _forward},
            TK_PACK,
            {'side': tk.LEFT, 'padx': 2}
        )
        
        self.stop_btn = TkinterWidgetBuilder(
            ttk.Button,
            {'master': self.controls, 'command': self.__stop_video, 'image': _stop},
            TK_PACK,
            {'side': tk.LEFT, 'padx': 2}
        )
        
        self.pause_btn = TkinterWidgetBuilder(
            ttk.Button,
            {'master': self.controls, 'command': self.__pause_video, 'image': _pause},
            TK_PACK,
            {'side': tk.LEFT, 'padx': 2}
        )
        
        self.volume_slider = TkinterWidgetBuilder(
            tk.Scale,
            {'master': self.controls, 'from_': 0, 'to': 100, 'orient': tk.HORIZONTAL, 'label': 'Volume', 'command': self.__set_volume},
            TK_PACK,
            {'side': tk.LEFT, 'padx': 2}
        )
        self.volume_slider.set(50)
        
        self.progress_value = tk.DoubleVar()
        self.progression_slider = TkinterWidgetBuilder(
            tk.Scale,
            {'master': self.controls, 'from_': 0, 'to': 100, 'showvalue': False, 'length': 600, 'orient': tk.HORIZONTAL, 'variable': self.progress_value},
            TK_PACK,
            {'side': tk.LEFT, 'padx': 2}
        )
        self.progression_slider.bind('<ButtonPress-1>', self.__on_slider_press)
        self.progression_slider.bind('<ButtonRelease-1>', self.__on_slider_release)
        self.current_media_label = ...
        
        # Keep Images!
        
        self.play_btn.image = _play
        self.stop_btn.image = _stop
        self.pause_btn.image = _pause
        self.ff_btn.image = _forward
        self.fb_btn.image = _backward
        
        self.__update_progress()
    
    def next_media(self): ...
    def last_media(self): ...
    
    def __set_video_panel(self): 
        """
        Wmbeds the VLC player's video output into the Tkinter video panel.
        It retrieves the window ID of the video panel and then assigns it to the VLC media player
        using platform-specific method: set_hwnd.
        """
        self.__player.set_hwnd(self.video_view.winfo_id())
        self.video_view.update_idletasks()
        
    def __play_video(self): 
        if not MediaPlayer._is_playing:
            Log('Play - MediaPlayer',logtype=LOG_INFO)
            self.__player.play()
            MediaPlayer._is_playing = True
            MediaPlayer._current_playing_instance = self
            
    def __pause_video(self): 
        Log('Pause - MediaPlayer',logtype=LOG_INFO)
        if MediaPlayer._current_playing_instance is not self: return
        MediaPlayer._current_playing_instance = None
        self.__player.pause()
        MediaPlayer._is_playing = False
        
    def __stop_video(self): 
        if MediaPlayer._current_playing_instance is not self: return
        MediaPlayer._current_playing_instance = None
        Log('Stop - MediaPlayer',logtype=LOG_INFO)
        self.__player.stop()
        MediaPlayer._is_playing = False
        
    def __set_volume(self, value): 
        self.vol = int(value)
        self.__player.audio_set_volume(self.vol)
        
    def __on_slider_press(self, event): 
        self.slider_dragging = True
        
    def __on_slider_release(self, event): 
        self.slider_dragging = False
        self.__seek_video()
        
    def __seek_video(self): 
        """
        Seeks the video to a new position based on the slider's value.
        The slider's value represents the time in milliseconds.
        """
        slider_value = self.progression_slider.get()
        self.__player.set_time(int(slider_value))
        
    def __update_progress(self): 
        """
        Updates the progress slider to reflect the current playback time.
        If the slider is not being manually adjusted by the user,
        this function retrieves the current playback time and the video's total length,
        updates the slider's range if necessary, and sets the slider to the current time.
        This function is called repeatedly every 500 milliseconds.
        """
        if not self.slider_dragging:

            current_time = self.__player.get_time()  # Current time in milliseconds.
            duration = self.__player.get_length()      # Total duration in milliseconds.
            if duration > 0:
                self.progression_slider.config(to=duration)
                self.progression_slider.set(current_time)

        self.after(500, self.__update_progress)
    
    def __end_fullscreen(self):
        self.attributes
    
    def open_file(self, videopath: str): 
        """
        Sets media to `video_path` in the VLC media player instance. Finally, it calls the method to embed
        the VLC video output into the Tkinter video panel.
        """
        #! BUG after running out of time it stops, but can't be revived by using: play or pause. The user must press stop
        if videopath:
            Log('Open file: $',[videopath],LOG_INFO)
            self.__stop_video()
            media = MediaPlayer._vlc_instance.media_new(videopath)
            self.__player.set_media(media)
            self.__set_video_panel()
        else:
            Log('Cannot open file: $',[videopath],LOG_WARNING)
    
class ImageWithSubtitleShow(tk.Canvas):
    def __init__(self,parent):
        super().__init__(parent)
        self.image_label = ttk.Label(parent)
        self.image_label.pack(pady=20)
        
        self.label = ttk.Label(parent)
        self.label.pack()
        
    def update_image(self, path: str, sub_title: str = ''):
        self.label.config(text = sub_title)
        self.image = Image.open(path).resize((512,288))
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.image,border=2,relief="raised")
        
def OutlineImage(bg: Image.Image, 
                 fg: Image.Image, 
                 width: int = 1, 
                 offset: tuple[int, int] = (0,0), 
                 fill_color: tuple[int, int, int] = (0, 0, 0)
                 ) -> Image.Image:
    """
    Will resize the bg image by {width}
    """
    bg_resized = bg.resize((bg.width + width, bg.height + width))
    
    _, _, _, alpha = bg_resized.split()
    
    # Create the threshold
    fill = Image.new("RGB", bg_resized.size, tuple(fill_color))
    result = Image.merge(
        "RGBA", 
        (fill.split()[0], 
                fill.split()[1], 
                fill.split()[2], 
                alpha)
        )
    
    # Background Offset
    canvas_w = max(bg_resized.width + abs(offset[0]), fg.width + width)
    canvas_h = max(bg_resized.height + abs(offset[1]), fg.height + width)
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    bg_x = (canvas_w - bg_resized.width) // 2 + offset[0]
    bg_y = (canvas_h - bg_resized.height) // 2 + offset[1]
    canvas.paste(result, (bg_x, bg_y), result)
    
    canvas.paste(fg, ((width // 2) + offset[0], (width // 2) + offset[1]), fg)
    return canvas

def RenderNumbers(text: str, font: str, size: float): 
    """ C:\\Windows\\Fonts\\{package}\\{ttf | otf} """
    if not text.isdecimal(): raise NotImplementedError
    font: ImageFont.FreeTypeFont = ImageFont.truetype(font, size)
    length = font.getlength(text)
    img = Image.new("RGBA",
              (int(length), size),
    (0,0,0,0))
    
    draw = ImageDraw.Draw(img)
    draw.text((0,0), text, font=font, fill=(255,255,255,255))
    return img

def RenderImageNumbers(text: str, font: dict[str, Image.Image]):
    if not text.isdecimal(): raise NotImplementedError
    char_size = font['0'].width
    length = len(text)
    
    img = Image.new("RGBA",
              (int(length * char_size), font['0'].height),
    (0,0,0,0))
    
    for i, char in enumerate(text):
        img.paste(font[char], (i * char_size, 0))
    return img

def GetTextNumbersFromImage(img: Image.Image) -> dict[str, Image.Image]:
    char_width = img.width // 10
    char_map = {}
    
    for i in range(10):
        _temp = Image.new("RGBA", (char_width, img.height), (0,0,0, 0))
        _temp.paste(img, (-i * char_width,0))
        char_map[str(i)] = _temp
    return char_map
       
class TGObject:
    def __init__(self, args: dict[str, Any]):
        self.args = args
        self.name = self.args['layer'].pop('name')
        _source = args['layer'].pop('source')
        self.source_type = _source['type']
        self.source_arg = _source['arg']
        self.get_position()
        self.get_rotation()
        self.get_scale()
        self.get_outline()

    def get_position(self): 
        if 'position' not in self.args['layer']: 
            self.position = (0.5, 0.5)
            return
        position = self.args['layer'].pop('position')
        x = position['x']
        y = position['y']
        
        rx = random.randint(
            int(x.get('from', 0) * 100), 
            int(x.get('to', 0) * 100)
            ) / 100
        
        ry = random.randint(
            int(y.get('from', 0) * 100), 
            int(y.get('to', 0) * 100)
            ) / 100
        
        self.position = x['default'] + rx, y['default'] + ry
        
    def get_scale(self): 
        if 'scale' not in self.args['layer']: 
            self.scale = 1.
            return
        scale = self.args['layer'].pop('scale')
        s = scale['default']
        
        rs = random.randint(
            int(scale.get('from', 0) * 100), 
            int(scale.get('to', 0) * 100)
            ) / 100
        
        self.scale = s + rs
    
    def get_rotation(self): 
        if 'rotation' not in self.args['layer']: 
            self.rotation = 0
            return
        rotation = self.args['layer'].pop('rotation')
        r = rotation['default']
        
        rr = random.randint(
            int(rotation.get('from', 0) * 100), 
            int(rotation.get('to', 0) * 100)
            ) / 100
        
        self.rotation = r + rr
    
    def get_outline(self):
        if 'outline' not in self.args['layer']: 
            self.outline = None
            return
        outline = self.args['layer'].pop('outline')
        self.outline = ((outline.get('x', 0), outline.get('y', 0)), outline.get('col', (0,0,0)), outline.get('width', 1))
    
    def get(self) -> Image.Image:
        ...

def RaiseExceptionOnCondition(cond: bool,msg: str, exc: Exception = AutomationError) -> None:
    """ raise_error_on_condition """
    if cond: raise exc(msg)

def GetVideoLength(filepath: str) -> float | None:
    time_or_error = FfmpegRunCommand(FFMPEG_GET_LENGTH,{'input_filepath': filepath},True)
    try:
        return float(time_or_error.replace('\n',''))
    except Exception as E:
        Log("$",[str(E)],LOG_ERROR)
        return None
    
def GetImageFromVideo(filepath: str, frame: int):
    if frame == -1: 
        _time = random.random() * GetVideoLength(filepath)
    else: 
        _time = frame
    Log("t: $ frame: $ fp: $",[_time,frame,filepath], LOG_INFO)
    RemoveIfExist(f'./temp.png')
    FfmpegRunCommand(FFMPEG_GET_FRAME,{'input_filepath': filepath, 'time': _time, 'output_filepath': './temp.png'})
    RaiseExceptionOnCondition(not path_os.isfile('./temp.png'), 'Something went wrong. File should exist.')
    return Image.open('./temp.png')

def CreateLibPngFile():
    if not path_os.isfile('libpng16-16.dll'):
        with open('libpng16-16.dll','wb') as fo:
            fo.write(LIBPNG16_16DLL)

class TGVideo(TGObject): 
    def __init__(self, args):
        super().__init__(args)
        self.video_path = ''
    
    def get(self):
        img = GetImageFromVideo(self.video_path, -1)
        return img if img is not None else Image.new("RGB", (600,600),(255,0,0))
        
class TGImage(TGObject): 
    def __init__(self, args):
        super().__init__(args)
    
    def get(self):
        return Image.open(self.source_arg)
        
class TGImageText(TGObject): 
    def __init__(self, args):
        super().__init__(args)
        self.number = '123'
    
    def get(self):
        img = Image.open(self.source_arg)
        return RenderImageNumbers(self.number, GetTextNumbersFromImage(img))
        
class ThumbnailGenerator: 
    def __init__(self, yml_ctx: str):
        self.yaml_context = yaml.safe_load(yml_ctx)
        self.layers: list[TGObject] = []
        self.__decomplicate_context()
        
    def __decomplicate_context(self):
        for layer in self.yaml_context:
            option = layer['layer']['source']
            _type, arg = option['type'], option['arg']
            layer: dict[str, Any]
            match _type:
                case 'video':
                    new_tg = TGVideo(layer)
                case 'image':
                    new_tg = TGImage(layer)
                case 'image_text':
                    new_tg = TGImageText(layer)
                case _:
                    raise NotImplementedError
            
            self.layers.append(new_tg)
            print(new_tg.name,new_tg.position,new_tg.scale,new_tg.rotation,new_tg.outline)
    
    def generate(self, video_path: str, episode_number: int | str, output_path: str):
        w, h = (1280, 720)
        mainframe = Image.new("RGBA", (w, h))
        for layer in self.layers:
            if isinstance(layer, TGVideo):
                layer.video_path = video_path
            elif isinstance(layer, TGImageText):
                layer.number = str(episode_number)
            _temp = layer.get()
            
            _temp: Image.Image
            _temp = _temp.rotate(layer.rotation)
            _temp = _temp.resize((int(_temp.width * layer.scale), int(_temp.height * layer.scale)))
            
            if layer.outline:
                _temp = OutlineImage(_temp, _temp, layer.outline[2], layer.outline[0], layer.outline[1])
            render_position = (int(layer.position[0] * w) - (_temp.width // 2), int(layer.position[1] * h) - (_temp.height // 2))
            mainframe.paste(_temp, render_position, _temp if _temp.mode == 'RGBA' else None)
        mainframe.save(output_path)
        
class SQLAccess: 
    Base = sql_declarative_base()
    database_url = 'sqlite:///lprt_data.db'
    _session = None
    _engine = None
    @staticmethod
    def create_session():
        SQLAccess._engine = sqlalchemy.create_engine(SQLAccess.database_url)
        SQLAccess.Base.metadata.create_all(SQLAccess._engine)
        SQLAccess._session = sql_sessionmaker(bind=SQLAccess._engine)()
        
    @staticmethod
    def _check_sql_alive(): 
        if SQLAccess._session is None or SQLAccess._engine is None:
            raise Exception("SQL is not initialized!")
    
    @staticmethod
    def read(table, **filter): 
        SQLAccess._check_sql_alive()
        SQLAccess._session.query(table).filter_by(**filter).all()

def ConvertGermanUmlautsToHtmlEntitys(): ...
def ConvertHTMLEntitysToGermanUmlauts(): ...