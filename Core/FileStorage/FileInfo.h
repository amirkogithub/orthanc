/**
 * Orthanc - A Lightweight, RESTful DICOM Store
 * Copyright (C) 2012-2013 Medical Physics Department, CHU of Liege,
 * Belgium
 *
 * This program is free software: you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * In addition, as a special exception, the copyright holders of this
 * program give permission to link the code of its release with the
 * OpenSSL project's "OpenSSL" library (or with modified versions of it
 * that use the same license as the "OpenSSL" library), and distribute
 * the linked executables. You must obey the GNU General Public License
 * in all respects for all of the code used other than "OpenSSL". If you
 * modify file(s) with this exception, you may extend this exception to
 * your version of the file(s), but you are not obligated to do so. If
 * you do not wish to do so, delete this exception statement from your
 * version. If you delete this exception statement from all source files
 * in the program, then also delete it here.
 * 
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 **/


#pragma once

#include <string>
#include <stdint.h>
#include "../Enumerations.h"

namespace Orthanc
{
  struct FileInfo
  {
  private:
    std::string uuid_;
    FileContentType contentType_;
    uint64_t uncompressedSize_;
    CompressionType compressionType_;
    uint64_t compressedSize_;

  public:
    FileInfo()
    {
    }

    /**
     * Constructor for an uncompressed attachment.
     **/
    FileInfo(const std::string& uuid,
             FileContentType contentType,
             uint64_t size) :
      uuid_(uuid),
      contentType_(contentType),
      uncompressedSize_(size),
      compressionType_(CompressionType_None),
      compressedSize_(size)
    {
    }

    /**
     * Constructor for a compressed attachment.
     **/
    FileInfo(const std::string& uuid,
             FileContentType contentType,
             uint64_t uncompressedSize,
             CompressionType compressionType,
             uint64_t compressedSize) :
      uuid_(uuid),
      contentType_(contentType),
      uncompressedSize_(uncompressedSize),
      compressionType_(compressionType),
      compressedSize_(compressedSize)
    {
    }

    const std::string& GetUuid() const
    {
      return uuid_;
    }

    FileContentType GetContentType() const
    {
      return contentType_;
    }

    uint64_t GetUncompressedSize() const
    {
      return uncompressedSize_;
    }

    CompressionType GetCompressionType() const
    {
      return compressionType_;
    }

    uint64_t GetCompressedSize() const
    {
      return compressedSize_;
    }
  };
}
