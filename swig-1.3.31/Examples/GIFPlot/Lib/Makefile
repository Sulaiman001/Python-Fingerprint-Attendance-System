CC      = gcc
CCSHARED= -fpic 
INCLUDES= -I../Include
CFLAGS  = -O
SRCS    = frame.c color.c plot2d.c plot3d.c font.c pixmap.c matrix.c gif.c
OBJS    = $(SRCS:.c=.o)
AR      = ar
RANLIB  = ranlib
TARGET  = ../libgifplot.a

.c.o: 
	$(CC) $(CCSHARED) $(INCLUDES) $(CFLAGS) -c -o $*.o $<

all:  $(OBJS)
	@rm -f ../libgifplot.a
	$(AR) cr $(TARGET) $(OBJS)
	$(RANLIB) $(TARGET)

clean:
	rm -f *.o *~ $(TARGET)

check: all
