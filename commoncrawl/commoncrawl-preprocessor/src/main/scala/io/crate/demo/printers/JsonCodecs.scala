package io.crate.demo.printers

import java.time.ZonedDateTime

import argonaut._, Argonaut._
import io.crate.demo.common.Page

object JsonCodecs {

  implicit def ZonedDateTimeCodecJson: CodecJson[ZonedDateTime] =
    CodecJson(
      (z: ZonedDateTime) => z.toString.asJson,
      z => for {isoStr <- z.as[String]} yield ZonedDateTime.parse(isoStr))



  implicit def PageCodecJson: CodecJson[Page] =
    casecodec6(Page.apply, Page.unapply)("uri", "ip", "date", "contentType", "contentLength", "content")
}
