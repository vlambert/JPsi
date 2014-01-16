CXX = $(shell root-config --cxx)
LD = $(shell root-config --ld)

OS_NAME:=$(shell uname -s | tr A-Z a-z)
ifeq ($(OS_NAME),darwin)
STDINCDIR := -I/opt/local/include
STDLIBDIR := -L/opt/local/lib
else
STDINCDIR := 
STDLIBDIR := 
endif

CPPFLAGS := $(shell root-config --cflags) $(STDINCDIR)
LDFLAGS := $(shell root-config --glibs) $(STDLIBDIR)

CPPFLAGS += -g

#TARGET = CorrFunctYYV3
#TARGET = PHOSPHOR_Functor
#TARGET = PHOSPHOR_CLOSURE	
TARGET = PHOSPHOR_Corr

#SRC = CreateGaussianSmearingNtuples.cc
#SRC = CreateClosureTestNtuples.cc PhosphorCorrectorFunctor.cc muon_corr_2011.cc
SRC = main.cc PhosphorCorrectorFunctor.cc

OBJ = $(SRC:.cc=.o)

all : $(TARGET)

$(TARGET) : $(OBJ)
	$(LD) $(CPPFLAGS) -o $(TARGET) $(OBJ) $(LDFLAGS)
	@echo $@
	@echo $<
	@echo $^

%.o : %.cc	
	$(CXX) $(CPPFLAGS) -o $@ -c $<
	@echo $@	
	@echo $<
clean :
	rm -f *.o $(TARGET) *~

