/* $Author: dblank $
 * $Name:  $
 * $Id: jpeg.h,v 1.1 2004/11/14 02:03:27 dblank Exp $
 * $Source: /home/CVS/pyro/camera/aibo/jpeg.h,v $
 * $Log: jpeg.h,v $
 * Revision 1.1  2004/11/14 02:03:27  dblank
 * From Player/Stage; jpeg_decompress
 *
 * Revision 1.1  2004/09/17 18:09:05  inspectorg
 * *** empty log message ***
 *
 * Revision 1.1  2004/09/10 05:34:14  natepak
 * Added a JpegStream driver
 *
 * Revision 1.2  2003/12/30 20:49:49  srik
 * Added ifdef flags for compatibility
 *
 * Revision 1.1.1.1  2003/12/30 20:39:19  srik
 * Helicopter deployment with firewire camera
 *
 */

#ifndef _JPEG_H_
#define _JPEG_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <jpeglib.h>
#include <jerror.h>
#include <setjmp.h>
struct my_error_mgr {
	struct jpeg_error_mgr pub;
	jmp_buf setjmp_buffer;
};

typedef struct my_error_mgr *my_error_ptr;


int 
jpeg_compress(char *dst, char *src, int width, int height, int dstsize, int quality);

void
jpeg_decompress(unsigned char *dst, int dst_size, unsigned char *src, int src_size);

void
jpeg_decompress_from_file(unsigned char *dst, char *file, int size, int *width, int *height);

#ifdef __cplusplus
}
#endif

#endif
