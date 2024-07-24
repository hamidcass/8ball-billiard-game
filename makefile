CC = clang
CFLAGS = -Wall -std=c99 -pedantic
PYTHON = python3.10

all: _phylib.so

phylib.py phylib_wrap.c: phylib.i
	swig -python phylib.i

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) -shared phylib_wrap.o -dynamiclib -L. -L/usr/lib/$(PYTHON) -l $(PYTHON) -lphylib -o _phylib.so

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -fPIC -I/usr/include/$(PYTHON) -o phylib_wrap.o

libphylib.so: phylib.o
	$(CC) $(CFLAGS) phylib.o -shared -lm -o libphylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o


clean: 
	rm -f *.o *.so *.svg

