import os
import unittest
import urllib2

from lxml import etree

from test.osctest import OscTest
from osc.httprequest import Urllib2HTTPRequest, HTTPError
from test.httptest import GET, PUT, POST, DELETE


def suite():
    return unittest.makeSuite(TestHTTPRequest)


class TestHTTPRequest(OscTest):
    def __init__(self, *args, **kwargs):
        kwargs['fixtures_dir'] = 'test_httprequest_fixtures'
        super(TestHTTPRequest, self).__init__(*args, **kwargs)

    def read_file(self, filename):
        return open(self.fixture_file(filename), 'r').read()

    @GET('http://localhost/source', text='foobar')
    def test_1(self):
        """simple get"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '', False)
        resp = r.get('/source')
        self.assertEqual(resp.read(), 'foobar')
        self.assertIsNone(resp._sio)

    @GET('http://localhost/source/server%3Amail?foo=bar&esc=foo%26bar',
         text='foobar')
    def test2(self):
        """simple get with query"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '', False)
        resp = r.get('/source/server:mail', foo='bar', esc='foo&bar')
        self.assertEqual(resp.read(), 'foobar')
        self.assertIsNone(resp._sio)

    @GET('http://localhost/source', file='prj_list.xml')
    def test3(self):
        """simple get with response validation"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '', False)
        resp = r.get('/source', schema=self.fixture_file('directory.xsd'))
        self.assertEqual(resp.read(), self.read_file('prj_list.xml'))
        self.assertIsNotNone(resp._sio)

    @GET('http://localhost/source', text='<foo />')
    def test4(self):
        """simple get with response validation (validation fails)"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '', False)
        self.assertRaises(etree.DocumentInvalid, r.get, '/source',
                          schema=self.fixture_file('directory.xsd'))

    @PUT('http://localhost/source/foo/bar/file', exp='this is a test',
         text='ok')
    def test5(self):
        """simple put"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '', False)
        resp = r.put('/source/foo/bar/file', data='this is a test')
        self.assertEqual(resp.read(), 'ok')
        self.assertIsNone(resp._sio)

    @PUT('http://localhost/source/foo/bar/file?x=foo+bar&foo=bar',
         expfile='putfile', text='ok',
         exp_content_type='application/octet-stream')
    def test6(self):
        """simple put (filename, uses mmap)"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '',
                               False, True, 20)
        resp = r.put('/source/foo/bar/file',
                     filename=self.fixture_file('putfile'),
                     x='foo bar', foo='bar')
        self.assertEqual(resp.read(), 'ok')
        self.assertIsNone(resp._sio)

    @POST('http://localhost/dummy', exp='simple+text', text='ok',
          exp_content_type='application/x-www-form-urlencoded')
    def test7(self):
        """simple post (urlencoded data)"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '', False)
        resp = r.post('/dummy', data='simple text', urlencoded=True)
        self.assertEqual(resp.read(), 'ok')
        self.assertIsNone(resp._sio)

    @POST('http://localhost/source/foo/bar/file?x=foo+bar&foo=bar',
          expfile='putfile', file='prj_list.xml',
          exp_content_type='application/octet-stream')
    def test8(self):
        """simple post (filename, uses mmap) - validate response"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '',
                               False, True, 20)
        resp = r.post('/source/foo/bar/file',
                      filename=self.fixture_file('putfile'),
                      schema=self.fixture_file('directory.xsd'),
                      x='foo bar', foo='bar')
        self.assertEqual(resp.read(), self.read_file('prj_list.xml'))
        self.assertIsNotNone(resp._sio)

    @POST('http://localhost/source/foo/bar/file?x=foo+bar&foo=bar',
          expfile='putfile', text='<somexml />',
          exp_content_type='application/octet-stream')
    def test9(self):
        """simple post (filename, uses mmap) - validation fails"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '',
                               False, True, 20)
        self.assertRaises(etree.DocumentInvalid, r.post,
                          '/source/foo/bar/file',
                          filename=self.fixture_file('putfile'),
                          schema=self.fixture_file('directory.xsd'),
                          x='foo bar', foo='bar')

    @DELETE('http://localhost/source/project', text='foobar')
    def test10(self):
        """simple delete"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '', False)
        resp = r.delete('/source/project')
        self.assertEqual(resp.read(), 'foobar')
        self.assertIsNone(resp._sio)

    @GET('http://localhost/source', text='foobar', header1='foo', x='42')
    def test11(self):
        """test response object"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '', False)
        resp = r.get('source')
        self.assertEqual(resp.url, 'http://localhost/source')
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.headers.get('header1'), 'foo')
        self.assertEqual(resp.headers['x'], '42')

    @GET('http://localhost/source',
         exception=urllib2.HTTPError('http://localhost/source', 403, 'error',
                                    {}, None))
    def test12(self):
        """test exception handling (get)"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '', False)
        self.assertRaises(HTTPError, r.get, 'source')

    @PUT('http://localhost/source', exp='foo bar',
         exception=urllib2.HTTPError('http://localhost/source', 400, 'error',
                                    {}, None))
    def test13(self):
        """test exception handling (put)"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '', False)
        self.assertRaises(HTTPError, r.put, 'source', data='foo bar')

    @GET('http://localhost/source',
         exception=urllib2.HTTPError('http://localhost/source', 403, 'error',
                                    {'foo': 'bar'}, None))
    def test14(self):
        """test exception handling (check exception object)"""
        r = Urllib2HTTPRequest('http://localhost', True, '', '', '', False)
        try:
            f = r.get('/source')
        except HTTPError as e:
            self.assertEqual(e.url, 'http://localhost/source')
            self.assertEqual(e.code, 403)
            self.assertEqual(e.headers['foo'], 'bar')
            self.assertIsNotNone(e.orig_exc)
        else:
            raise AssertionError()

if __name__ == '__main__':
    unittest.main()
