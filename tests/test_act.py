from unittest import TestCase
from nose.tools import *  # noqa
from datetime import date

from cobalt.act import Act, datestring, AmendmentEvent, RepealEvent

class ActTestCase(TestCase):
    def test_empty_act(self):
        a = Act()
        assert_equal(a.title, "Untitled")
        assert_is_not_none(a.meta)
        assert_is_not_none(a.body)

    def test_frbr_uri(self):
        a = Act()
        a.expression_date = '2012-01-01'
        a.frbr_uri = '/zm/act/2007/01'

        assert_equal(a.frbr_uri.work_uri(), '/zm/act/2007/01')
        assert_equal(a.number, '01')

        assert_equal(a.meta.identification.FRBRWork.FRBRthis.get('value'), '/zm/act/2007/01/main')
        assert_equal(a.meta.identification.FRBRWork.FRBRuri.get('value'), '/zm/act/2007/01')
        assert_equal(a.meta.identification.FRBRWork.FRBRcountry.get('value'), 'zm')

        assert_equal(a.meta.identification.FRBRExpression.FRBRthis.get('value'), '/zm/act/2007/01/eng@2012-01-01/main')
        assert_equal(a.meta.identification.FRBRExpression.FRBRuri.get('value'), '/zm/act/2007/01/eng@2012-01-01')

        assert_equal(a.meta.identification.FRBRManifestation.FRBRthis.get('value'), '/zm/act/2007/01/eng@2012-01-01/main')
        assert_equal(a.meta.identification.FRBRManifestation.FRBRuri.get('value'), '/zm/act/2007/01/eng@2012-01-01')
        

    def test_empty_body(self):
        a = Act()
        assert_not_equal(a.body_xml, '')
        a.body_xml = ''
        assert_not_equal(a.body_xml, '')

    def test_work_date(self):
        a = Act()
        a.work_date = '2012-01-02'
        assert_equal(datestring(a.work_date), '2012-01-02')
        assert_is_instance(a.work_date, date)

    def test_expression_date(self):
        a = Act()
        a.expression_date = '2012-01-02'
        assert_equal(datestring(a.expression_date), '2012-01-02')
        assert_is_instance(a.expression_date, date)

    def test_manifestation_date(self):
        a = Act()
        a.manifestation_date = '2012-01-02'
        assert_equal(datestring(a.manifestation_date), '2012-01-02')
        assert_is_instance(a.manifestation_date, date)

    def test_publication_date(self):
        a = Act()
        assert_is_none(a.publication_date)

        a.publication_date = '2012-01-02'
        assert_equal(datestring(a.publication_date), '2012-01-02')
        assert_is_instance(a.publication_date, date)

    def test_publication_number(self):
        a = Act()
        assert_is_none(a.publication_number)

        a.publication_number = '1234'
        assert_equal(a.publication_number, '1234')

    def test_publication_name(self):
        a = Act()
        assert_is_none(a.publication_name)

        a.publication_name = 'Publication'
        assert_equal(a.publication_name, 'Publication')

    def test_language(self):
        a = Act()
        a.language = 'fre'
        assert_equal(a.language, 'fre')

    def test_table_of_contents(self):
        a = Act()
        a.body_xml = """
        <body xmlns="http://www.akomantoso.org/2.0">
          <section id="section-1">
            <num>1.</num>
            <heading>Foo</heading>
            <content>
              <p>hello</p>
            </content>
          </section>
          <chapter id="chapter-1">
            <num>1.</num>
            <heading>The Chapter</heading>
            <part id="part-A">
              <num>A</num>
              <heading>The Part</heading>
              <section id="section-2">
                <num>2.</num>
                <heading>Other</heading>
                <content>
                  <p>hi</p>
                </content>
              </section>
            </part>
          </chapter>
        </body>
        """
        toc = a.table_of_contents()
        toc = [t.as_dict() for t in toc]
        self.maxDiff = None
        self.assertEqual(toc, [
            {'id': 'section-1', 'num': '1.', 'type': 'section', 'heading': 'Foo',
              'component': 'main', 'subcomponent': 'section/1', 'title': '1. Foo'},
            {'id': 'chapter-1', 'num': '1.', 'type': 'chapter', 'heading': 'The Chapter',
              'component': 'main', 'subcomponent': 'chapter/1', 'title': 'Chapter 1. - The Chapter', 'children': [
                {'id': 'part-A', 'num': 'A', 'type': 'part', 'heading': 'The Part',
                  'component': 'main', 'subcomponent': 'chapter/1/part/A', 'title': 'Part A - The Part', 'children': [
                    {'id': 'section-2', 'num': '2.', 'type': 'section', 'heading': 'Other',
                      'component': 'main', 'subcomponent': 'section/2', 'title': '2. Other'},
                    ]
                },
                ]
            },
            ])

    def test_component_table_of_contents(self):
        a = Act("""
<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <act contains="singleVersion">
    <meta>
      <identification source="#openbylaws">
        <FRBRWork>
          <FRBRthis value="/za/by-law/cape-town/2002/community-fire-safety/main"/>
          <FRBRuri value="/za/by-law/cape-town/2002/community-fire-safety"/>
          <FRBRalias value="Community Fire Safety By-law"/>
          <FRBRdate date="2002-02-28" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRcountry value="za"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/za/by-law/cape-town/2002/community-fire-safety/main/eng@"/>
          <FRBRuri value="/za/by-law/cape-town/2002/community-fire-safety/eng@"/>
          <FRBRdate date="2002-02-28" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/za/by-law/cape-town/2002/community-fire-safety/main/eng@"/>
          <FRBRuri value="/za/by-law/cape-town/2002/community-fire-safety/eng@"/>
          <FRBRdate date="2014-01-14" name="Generation"/>
          <FRBRauthor href="#openbylaws" as="#author"/>
        </FRBRManifestation>
      </identification>
    </meta>
    <body></body>
  </act>
  <components>
    <component id="component-1">
      <doc name="schedule1">
        <meta>
          <identification source="#slaw">
            <FRBRWork>
              <FRBRthis value="/za/act/1980/01/schedule1"/>
              <FRBRuri value="/za/act/1980/01"/>
              <FRBRalias value="A Title"/>
              <FRBRdate date="1980-01-01" name="Generation"/>
              <FRBRauthor href="#council" as="#author"/>
              <FRBRcountry value="za"/>
            </FRBRWork>
            <FRBRExpression>
              <FRBRthis value="/za/act/1980/01/eng@/schedule1"/>
              <FRBRuri value="/za/act/1980/01/eng@"/>
              <FRBRdate date="1980-01-01" name="Generation"/>
              <FRBRauthor href="#council" as="#author"/>
              <FRBRlanguage language="eng"/>
            </FRBRExpression>
            <FRBRManifestation>
              <FRBRthis value="/za/act/1980/01/eng@/schedule1"/>
              <FRBRuri value="/za/act/1980/01/eng@"/>
              <FRBRdate date="2015-04-22" name="Generation"/>
              <FRBRauthor href="#slaw" as="#author"/>
            </FRBRManifestation>
          </identification>
        </meta>
        <mainBody>
          <section id="schedule-1.section-0">
            <content>
              <p>1. Foo</p>
              <p>2. Bar</p>
            </content>
          </section>
        </mainBody>
      </doc>
    </component>
    <component id="component-2">
      <doc name="schedule2">
        <meta>
          <identification source="#slaw">
            <FRBRWork>
              <FRBRthis value="/za/act/1980/01/schedule2"/>
              <FRBRuri value="/za/act/1980/01"/>
              <FRBRdate date="1980-01-01" name="Generation"/>
              <FRBRauthor href="#council" as="#author"/>
              <FRBRcountry value="za"/>
            </FRBRWork>
            <FRBRExpression>
              <FRBRthis value="/za/act/1980/01/eng@/schedule2"/>
              <FRBRuri value="/za/act/1980/01/eng@"/>
              <FRBRdate date="1980-01-01" name="Generation"/>
              <FRBRauthor href="#council" as="#author"/>
              <FRBRlanguage language="eng"/>
            </FRBRExpression>
            <FRBRManifestation>
              <FRBRthis value="/za/act/1980/01/eng@/schedule2"/>
              <FRBRuri value="/za/act/1980/01/eng@"/>
              <FRBRdate date="2015-04-22" name="Generation"/>
              <FRBRauthor href="#slaw" as="#author"/>
            </FRBRManifestation>
          </identification>
        </meta>
        <mainBody>
          <section id="schedule-2.section-0">
            <content>
              <p>Baz</p>
              <p>Boom</p>
            </content>
          </section>
        </mainBody>
      </doc>
    </component>
  </components>
</akomaNtoso>
        """)
        toc = a.table_of_contents()
        toc = [t.as_dict() for t in toc]
        self.maxDiff = None
        self.assertEqual([
          {'component': 'schedule1', 'type': 'doc', 'subcomponent': None, 'heading': 'A Title', 'title': 'A Title', 'children': [
            {'component': 'schedule1', 'type': 'section', 'id': 'schedule-1.section-0', 'subcomponent': 'section', 'title': 'Section'}]},
          {'component': 'schedule2', 'type': 'doc', 'subcomponent': None, 'heading': 'Schedule 2', 'title': 'Schedule 2', 'children': [
            {'component': 'schedule2', 'type': 'section', 'id': 'schedule-2.section-0', 'subcomponent': 'section', 'title': 'Section'}]},
        ], toc)

    def test_preamble_and_friends_in_table_of_contents(self):
        a = Act(act_fixture("""
        <coverpage>
            <content><p>hi</p></content>
        </coverpage>
        <preface>
            <content><p>hi</p></content>
        </preface>
        <preamble>
            <content><p>hi</p></content>
        </preamble>
        <body>
            <content><p>hi</p></content>
        </body>
        <conclusions>
            <content><p>hi></p></content>
        </conclusions>
        """))

        toc = a.table_of_contents()
        toc = [t.as_dict() for t in toc]
        self.maxDiff = None
        self.assertEqual(toc, [
            {'type': 'coverpage', 'component': 'main', 'subcomponent': 'coverpage', 'title': 'Coverpage'},
            {'type': 'preface', 'component': 'main', 'subcomponent': 'preface', 'title': 'Preface'},
            {'type': 'preamble', 'component': 'main', 'subcomponent': 'preamble', 'title': 'Preamble'},
            {'type': 'conclusions', 'component': 'main', 'subcomponent': 'conclusions', 'title': 'Conclusions'},
            ])

    def test_get_subcomponent(self):
        a = Act()
        a.body_xml = """
        <body xmlns="http://www.akomantoso.org/2.0">
          <section id="section-1">
            <num>1.</num>
            <heading>Foo</heading>
            <content>
              <p>hello</p>
            </content>
          </section>
          <chapter id="chapter-2">
            <num>2.</num>
            <heading>The Chapter</heading>
            <content>
              <p>hi</p>
            </content>
          </chapter>
        </body>
        """

        assert_is_not_none(a.components()['main'])
        elem = a.get_subcomponent('main', 'chapter/2')
        assert_equal(elem.get('id'), "chapter-2")

        elem = a.get_subcomponent('main', 'section/1')
        assert_equal(elem.get('id'), "section-1")

        assert_is_none(a.get_subcomponent('main', 'chapter/99'))
        assert_is_none(a.get_subcomponent('main', 'section/99'))

    def test_set_amendments(self):
        a = Act()
        a.body_xml = """
        <body xmlns="http://www.akomantoso.org/2.0"/>
        """

        a.amendments = [AmendmentEvent(date='2012-02-01', amending_uri='/za/act/1980/10', amending_title="Foo")]

        assert_equal(a.to_xml(), """<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <act contains="singleVersion">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/za/act/1900/1/main"/>
          <FRBRuri value="/za/act/1900/1"/>
          <FRBRalias value="Untitled"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRcountry value="za"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/za/act/1900/1/eng@/main"/>
          <FRBRuri value="/za/act/1900/1/eng@"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/za/act/1900/1/eng@/main"/>
          <FRBRuri value="/za/act/1900/1/eng@"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
        </FRBRManifestation>
      </identification>
      <lifecycle source="#cobalt">
        <eventRef id="amendment-2012-02-01" date="2012-02-01" type="amendment" source="#amendment-0-source"/>
      </lifecycle>
      <references>
        <TLCOrganization id="cobalt" href="https://github.com/Code4SA/cobalt" showAs="cobalt"/>
        <passiveRef id="amendment-0-source" href="/za/act/1980/10" showAs="Foo"/>
      </references>
    </meta>
    <body/>
  </act>
</akomaNtoso>
""")

        a.amendments = [
            AmendmentEvent(date='2012-02-01', amending_uri='/za/act/1980/22', amending_title="Corrected"),
            AmendmentEvent(date='2013-03-03', amending_uri='/za/act/1990/5', amending_title="Bar"),
        ]
        assert_equals(a.to_xml(), """<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <act contains="singleVersion">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/za/act/1900/1/main"/>
          <FRBRuri value="/za/act/1900/1"/>
          <FRBRalias value="Untitled"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRcountry value="za"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/za/act/1900/1/eng@/main"/>
          <FRBRuri value="/za/act/1900/1/eng@"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/za/act/1900/1/eng@/main"/>
          <FRBRuri value="/za/act/1900/1/eng@"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
        </FRBRManifestation>
      </identification>
      <lifecycle source="#cobalt">
        <eventRef id="amendment-2012-02-01" date="2012-02-01" type="amendment" source="#amendment-0-source"/>
        <eventRef id="amendment-2013-03-03" date="2013-03-03" type="amendment" source="#amendment-1-source"/>
      </lifecycle>
      <references>
        <TLCOrganization id="cobalt" href="https://github.com/Code4SA/cobalt" showAs="cobalt"/>
        <passiveRef id="amendment-0-source" href="/za/act/1980/22" showAs="Corrected"/>
        <passiveRef id="amendment-1-source" href="/za/act/1990/5" showAs="Bar"/>
      </references>
    </meta>
    <body/>
  </act>
</akomaNtoso>
""")

        amendment = a.amendments[0]
        assert_equal(datestring(amendment.date), '2012-02-01')
        assert_equal(amendment.amending_uri, '/za/act/1980/22')
        assert_equal(amendment.amending_title, 'Corrected')

        amendment = a.amendments[1]
        assert_equal(datestring(amendment.date), '2013-03-03')
        assert_equal(amendment.amending_uri, '/za/act/1990/5')
        assert_equal(amendment.amending_title, 'Bar')

    def test_set_repeal(self):
        a = Act()
        a.body_xml = """
        <body xmlns="http://www.akomantoso.org/2.0"/>
        """

        a.repeal = RepealEvent(date='2012-02-01', repealing_uri='/za/act/1980/10', repealing_title='Foo')

        assert_equal(a.to_xml(), """<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <act contains="originalVersion">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/za/act/1900/1/main"/>
          <FRBRuri value="/za/act/1900/1"/>
          <FRBRalias value="Untitled"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRcountry value="za"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/za/act/1900/1/eng@/main"/>
          <FRBRuri value="/za/act/1900/1/eng@"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/za/act/1900/1/eng@/main"/>
          <FRBRuri value="/za/act/1900/1/eng@"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
        </FRBRManifestation>
      </identification>
      <lifecycle source="#cobalt">
        <eventRef id="repeal-2012-02-01" date="2012-02-01" type="repeal" source="#repeal-source"/>
      </lifecycle>
      <references>
        <TLCOrganization id="cobalt" href="https://github.com/Code4SA/cobalt" showAs="cobalt"/>
        <passiveRef id="repeal-source" href="/za/act/1980/10" showAs="Foo"/>
      </references>
    </meta>
    <body/>
  </act>
</akomaNtoso>
""")

        assert_equal(a.repeal.repealing_uri, '/za/act/1980/10')
        assert_equal(a.repeal.repealing_title, 'Foo')
        assert_equal(datestring(a.repeal.date), '2012-02-01')

        # check that clearing it works
        a.repeal = None
        assert_is_none(a.repeal)


def act_fixture(content):
    return """<?xml version="1.0"?>
<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <act contains="originalVersion">
    <meta>
      <identification source="">
        <FRBRWork>
          <FRBRthis value="/za/act/1900/1/main"/>
          <FRBRuri value="/za/act/1900/1"/>
          <FRBRalias value="Untitled"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRcountry value="za"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/za/act/1900/1/eng@/main"/>
          <FRBRuri value="/za/act/1900/1/eng@"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/za/act/1900/1/eng@/main"/>
          <FRBRuri value="/za/act/1900/1/eng@"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
        </FRBRManifestation>
      </identification>
    </meta>
    %s
  </act>
</akomaNtoso>""" % content
