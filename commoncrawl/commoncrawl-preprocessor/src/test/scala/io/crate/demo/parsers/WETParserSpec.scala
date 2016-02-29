package io.crate.demo.parsers

import java.time.{ZoneId, ZonedDateTime}

import io.crate.demo.WETParser

import org.scalatest._
import scala.io.Source


class WETParserSpec extends FlatSpec with Matchers {
  val wetExampleSkip = "WARC/1.0\n" +
    "WARC-Type: some-other-type\n" +
    "WARC-Target-URI: http://example.com/a?x=y&l=2\n" +
    "WARC-Date: 2015-08-27T19:33:34Z\n" +
    "WARC-Record-ID: <urn:uuid:0c17651c-c46c-4141-8a34-041b672ecc23>\n" +
    "WARC-Refers-To: <urn:uuid:38845fb8-2c43-4f97-b37b-99acacf7a952>\n" +
    "WARC-Block-Digest: sha1:W76WWFQIRQGQNOOMAVWPVI3AUZ62DDWQ\n" +
    "Content-Type: text/plain\n" +
    "Content-Length: 11\n\n" +
    "Hello World"


  val wetExample = "WARC/1.0\n" +
    "WARC-Type: conversion\n" +
    "WARC-Target-URI: http://example.com/a?x=y&l=2\n" +
    "WARC-Date: 2015-08-27T19:33:34Z\n" +
    "WARC-Record-ID: <urn:uuid:0c17651c-c46c-4141-8a34-041b672ecc23>\n" +
    "WARC-Refers-To: <urn:uuid:38845fb8-2c43-4f97-b37b-99acacf7a952>\n" +
    "WARC-Block-Digest: sha1:W76WWFQIRQGQNOOMAVWPVI3AUZ62DDWQ\n" +
    "Content-Type: text/plain\n" +
    "Content-Length: 11\n\n" +
    "Hello World"

  val wetExampleNoWarc = "WARC-Type: conversion\n" +
    "WARC-Target-URI: http://example.com/a?x=y&l=2\n" +
    "WARC-Date: 2015-08-27T19:33:34Z\n" +
    "WARC-Record-ID: <urn:uuid:0c17651c-c46c-4141-8a34-041b672ecc23>\n" +
    "WARC-Refers-To: <urn:uuid:38845fb8-2c43-4f97-b37b-99acacf7a952>\n" +
    "WARC-Block-Digest: sha1:W76WWFQIRQGQNOOMAVWPVI3AUZ62DDWQ\n" +
    "Content-Type: text/plain\n" +
    "Content-Length: 11\n\n" +
    "Hello World"


  def aParserFor(sourceStr: String) = new WETParser {
    override val source: Source = Source.fromString(sourceStr)
  }

  "A WETParser" should "parse fully WARC-Type conversation" in {
    val parsed = aParserFor(wetExample).map(p => p).toIndexedSeq
    parsed.size should ===(1)
    val parsedObj = parsed(0)
    parsedObj.content should ===("Hello World")
    parsedObj.contentLength should ===(11)
    parsedObj.date should ===("2015-08-27T19:33:34Z")
    parsedObj.contentType should ===("text/plain")
    parsedObj.uri should ===("http://example.com/a?x=y&l=2")
    parsedObj.domain should ===("example.com")
    parsedObj.reverseDomain should ===("com.example")
  }

  "A WETParser" should "ignore any other WARC-Type" in {
    val parsed = aParserFor(wetExampleSkip + wetExample).toList
    parsed.size should ===(1)
    val parsedObj = parsed(0)
    parsedObj.content should ===("Hello World")
    parsedObj.contentLength should ===(11)
    parsedObj.date should ===("2015-08-27T19:33:34Z")
    parsedObj.contentType should ===("text/plain")
    parsedObj.uri should ===("http://example.com/a?x=y&l=2")
    parsedObj.domain should ===("example.com")
    parsedObj.reverseDomain should ===("com.example")

  }

  "A WETParser" should "use WARC/1.0 as delimiter for WET blocks" in {
    val parsed = aParserFor(wetExample + wetExampleNoWarc).toList
    parsed.size should ===(1)
  }
}