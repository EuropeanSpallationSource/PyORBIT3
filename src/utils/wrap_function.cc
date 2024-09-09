#include "orbit_mpi.hh"
#include "pyORBIT_Object.hh"

#include "wrap_utils.hh"
#include "wrap_function.hh"

#include <iostream>
#include <string>

#include "OU_Function.hh"

using namespace OrbitUtils;
using namespace wrap_orbit_utils;

namespace wrap_function{

  void error(const char* msg){ ORBIT_MPI_Finalize(msg); }

#ifdef __cplusplus
extern "C" {
#endif

	/**
	    Constructor for python class wrapping c++ Function instance.
      It never will be called directly.
	*/
	static PyObject* Function_new(PyTypeObject *type, PyObject *args, PyObject *kwds){
		pyORBIT_Object* self;
		self = (pyORBIT_Object *) type->tp_alloc(type, 0);
		self->cpp_obj = NULL;
		return (PyObject *) self;
	}

  /** This is implementation of the __init__ method */
  static int Function_init(pyORBIT_Object *self, PyObject *args, PyObject *kwds){
	  self->cpp_obj =  new Function();
	  ((Function*) self->cpp_obj)->setPyWrapper((PyObject*) self);
    return 0;
  }

	/** It will return Python Lists with x_arr, y_arr, err_arr */
  static PyObject* Function_getLists(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
	  int size = cpp_Function->getSize();
	  PyObject* xPyList = PyList_New(size);
	  PyObject* yPyList = PyList_New(size);
	  PyObject* errPyList = PyList_New(size);
	  for(int ind = 0; ind < size; ind++){
			if(PyList_SetItem(xPyList,ind,Py_BuildValue("d",cpp_Function->x(ind))) != 0){
				error("pyFunction: getLists(...)  cannot create a resulting list for x_arr.");
			}
			if(PyList_SetItem(yPyList,ind,Py_BuildValue("d",cpp_Function->y(ind))) != 0){
				error("pyFunction: getLists(...)  cannot create a resulting list for y_arr.");
			}
			if(PyList_SetItem(errPyList,ind,Py_BuildValue("d",cpp_Function->err(ind))) != 0){
				error("pyFunction: getLists(...)  cannot create a resulting list for err_arr.");
			}
	  }
	  PyObject* pyRes = PyTuple_New(3);
	  if(PyTuple_SetItem(pyRes,0,xPyList) != 0){
	  	error("pyFunction: getLists(...)  cannot put x_arr into resulting tuple.");
	  }
	  if(PyTuple_SetItem(pyRes,1,yPyList) != 0){
	  	error("pyFunction: getLists(...)  cannot put y_arr into resulting tuple.");
	  }
	  if(PyTuple_SetItem(pyRes,2,errPyList) != 0){
	  	error("pyFunction: getLists(...)  cannot put err_arr into resulting tuple.");
	  }
		return pyRes;
  }

	/** It will init Function with Lists of x_arr, y_arr, err_arr */
  static PyObject* Function_addLists(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
	  cpp_Function->cleanMemory();
	  PyObject* xPyList = NULL;
	  PyObject* yPyList = NULL;
	  PyObject* errPyList = NULL;
	  int errPyList_was_null = 0;
	  int size = 0;
		if(!PyArg_ParseTuple(	args,"OO|O:",&xPyList,&yPyList,&errPyList))
			error("pyFunction addLists(x_arr,y_arr) or addLists(x_arr,y_arr,err_arr) - parameters are needed");
		else{
			if(PyList_Check(xPyList) == 0 || PyList_Check(yPyList) == 0)
				error("pyFunction addLists(x_arr,y_arr) or addLists(x_arr,y_arr,err_arr) - parameters are not pyLists.");
			size = PyList_Size(xPyList);
			if(size != PyList_Size(yPyList)){
				error("pyFunction addLists(x_arr,y_arr) or addLists(x_arr,y_arr,err_arr) - len(x_arr) != len(y_arr).");
			}
			if(errPyList == NULL){
				errPyList_was_null = 1;
				errPyList = PyList_New(size);
				for(int ind = 0; ind < size; ind++){
					if(PyList_SetItem(errPyList,ind,Py_BuildValue("d",0.)) != 0)
						error("pyFunction: addLists(...)  cannot create a zero values list for err_arr.");
				}
			} else {
				if(PyList_Check(errPyList) == 0 || size != PyList_Size(errPyList))
					error("pyFunction addLists(x_arr,y_arr,err_arr) - err_arr parameters is not correct pyLists.");
			}
			for(int ind = 0; ind < size; ind++){
				double x = PyFloat_AsDouble(PyList_GetItem(xPyList,ind));
				double y = PyFloat_AsDouble(PyList_GetItem(yPyList,ind));
				double err = PyFloat_AsDouble(PyList_GetItem(errPyList,ind));
				cpp_Function->add(x,y,err);
			}
		}
		if(errPyList_was_null == 1) Py_DECREF(errPyList);
	 	Py_INCREF(Py_None);
		return Py_None;
	}

	/** It will add (x,y) or (x,y,err) point to the Function instance */
  static PyObject* Function_add(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
	  double x,y;
		double err = 0.;
		if(!PyArg_ParseTuple(	args,"dd|d:",&x,&y,&err))
			error("pyFunction add(x,y) or add(x,y,err) - parameters are needed");
		else {
			cpp_Function->add(x,y,err);
		}
		Py_INCREF(Py_None);
		return Py_None;
  }

 	/** It will return the number of (x,y) pairs in the Function instance */
  static PyObject* Function_getSize(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
	  int size = cpp_Function->getSize();
		return Py_BuildValue("i",size);
  }

 	/** It will return x for a particular index ind */
  static PyObject* Function_x(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		int ind = -1;
		if(!PyArg_ParseTuple(	args,"i:",&ind)){
			error("pyFunction x(index) - parameter is needed");
		}
		return Py_BuildValue("d",cpp_Function->x(ind));
  }

 	/** It will return y for a particular index ind */
  static PyObject* Function_y(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		int ind = -1;
		if(!PyArg_ParseTuple(	args,"i:",&ind)){
			error("pyFunction y(index) - parameter is needed");
		}
		return Py_BuildValue("d",cpp_Function->y(ind));
  }


 	/** It will return y for a particular index */
  static PyObject* Function_err(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		int ind = -1;
		if(!PyArg_ParseTuple(	args,"i:",&ind)){
			error("pyFunction err(index) - parameter is needed");
		}
		return Py_BuildValue("d",cpp_Function->err(ind));
  }

 	/** It will return (x,y) for a particular index ind */
  static PyObject* Function_xy(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		int ind = -1;
		if(!PyArg_ParseTuple(	args,"i:",&ind)){
			error("pyFunction xy(index) - parameter is needed");
		}
		return Py_BuildValue("(dd)",cpp_Function->x(ind),cpp_Function->y(ind));
  }

 	/** It will return (x,y) for a particular index ind */
  static PyObject* Function_xyErr(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		int ind = -1;
		if(!PyArg_ParseTuple(	args,"i:",&ind)){
			error("pyFunction xyErr(index) - parameter is needed");
		}
		return Py_BuildValue("(ddd)",cpp_Function->x(ind),cpp_Function->y(ind),cpp_Function->err(ind));
  }

 	/** It will remove a point with a particular index */
  static PyObject* Function_removePoint(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		int ind = -1;
		if(!PyArg_ParseTuple(	args,"i:",&ind)){
			error("pyFunction removePoint(index) - parameter is needed");
		}
		cpp_Function->removePoint(ind);
	 	Py_INCREF(Py_None);
		return Py_None;
  }

	/** It will update (y) or (y,err) values for the point with index = index */
  static PyObject* Function_updatePoint(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
	  int ind = -1;
	  double y;
		double err = 0.;
		if(!PyArg_ParseTuple(	args,"id|d:",&ind,&y,&err))
			error("pyFunction updatePoint(ind,y) or updatePoint(ind,y,err) - parameters are needed");
		else {
			cpp_Function->updatePoint(ind,y,err);
		}
		Py_INCREF(Py_None);
		return Py_None;
  }

 	/** It will return minimal x value in the Function */
  static PyObject* Function_getMinX(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		return Py_BuildValue("d",cpp_Function->getMinX());
  }

 	/** It will return maximal x value in the Function */
  static PyObject* Function_getMaxX(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		return Py_BuildValue("d",cpp_Function->getMaxX());
  }

 	/** It will return minimal y value in the Function */
  static PyObject* Function_getMinY(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		return Py_BuildValue("d",cpp_Function->getMinY());
  }

 	/** It will return maximal y value in the Function */
  static PyObject* Function_getMaxY(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		return Py_BuildValue("d",cpp_Function->getMaxY());
  }

 	/** It will remove all points in the Function */
  static PyObject* Function_clean(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		cpp_Function->clean();
	 	Py_INCREF(Py_None);
		return Py_None;
  }

 	/** It will free the memeory and will remove all points in the Function */
  static PyObject* Function_cleanMemory(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		cpp_Function->cleanMemory();
	 	Py_INCREF(Py_None);
		return Py_None;
  }

 	/** It will return y for a specified x value */
  static PyObject* Function_getY(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		double val = 0.;
		if(!PyArg_ParseTuple(	args,"d:",&val)){
			error("pyFunction getY(x) - parameter is needed");
		}
		return Py_BuildValue("d",cpp_Function->getY(val));
  }

 	/** It will return dy/dx for a specified x value */
  static PyObject* Function_getYP(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		double val = 0.;
		if(!PyArg_ParseTuple(	args,"d:",&val)){
			error("pyFunction getYP(x) - parameter is needed");
		}
		return Py_BuildValue("d",cpp_Function->getYP(val));
  }

 	/** It will return x for a specified y value */
  static PyObject* Function_getX(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		double val = 0.;
		if(!PyArg_ParseTuple(	args,"d:",&val)){
			error("pyFunction getX(y) - parameter is needed");
		}
		return Py_BuildValue("d",cpp_Function->getX(val));
  }

 	/** It will return x for a specified y value */
  static PyObject* Function_getYErr(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		double val = 0.;
		if(!PyArg_ParseTuple(	args,"d:",&val)){
			error("pyFunction getYErr(y) - parameter is needed");
		}
		return Py_BuildValue("d",cpp_Function->getYErr(val));
  }

 	/** It will set the constant step flag to 1 if it is possible */
  static PyObject* Function_setConstStep(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		int inf = -1;
		if(!PyArg_ParseTuple(	args,"i:",&inf)){
			error("pyFunction setConstStep(inf) - parameter is needed");
		}
		return Py_BuildValue("i",cpp_Function->setConstStep(inf));
  }

 	/** It will return 1 if the step is const and 0 otherwise */
  static PyObject* Function_isStepConst(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		return Py_BuildValue("i",cpp_Function->isStepConst());
  }

  /** It will return the constant step tolerance for x variable */
  static PyObject* Function_getStepEps(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		return Py_BuildValue("d",cpp_Function->getStepEps());
  }

  /** It will set the constant step tolerance for x variable */
  static PyObject* Function_setStepEps(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
	  double eps;
		if(!PyArg_ParseTuple(	args,"d:",&eps)){
			error("pyFunction setStepEps(eps) - parameter is needed");
		}
		cpp_Function->setStepEps(eps);
		return Py_BuildValue("d",cpp_Function->getStepEps());
  }

 	/** It will build the reverse Function if it is possible and return 1 or 0 */
  static PyObject* Function_setInverse(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		Function* rf = NULL;
	  PyObject* pyF;
		int inf = -1;
		if(!PyArg_ParseTuple(	args,"O:",&pyF))
			error("pyFunction setInverse(pyFunction F) - parameter is needed");
		else {
			PyObject* pyORBIT_Function_Type = getOrbitUtilsType("Function");
			if(!PyObject_IsInstance(pyF,pyORBIT_Function_Type)){
				error("pyFunction - setInverse(pyFunction F) - pyFunction parameter is needed.");
			}
			rf= (Function*) ((pyORBIT_Object*) pyF)->cpp_obj;
			inf = cpp_Function->setInverse(rf);
		}
		return Py_BuildValue("i",inf);
  }

  //Prints Function into the std::cout stream or file
  static PyObject* Function_dump(PyObject *self, PyObject *args){
		Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
    //if nVars == 0 print into std::cout
    //if nVars == 1 print into the file
    int nVars = PyTuple_Size(args);
    const char* file_name = NULL;
    if(nVars == 0 ||  nVars == 1){
      if(nVars == 0){
        cpp_Function->print(std::cout);
      }
      else{
        if(!PyArg_ParseTuple(	args,"s:dump",&file_name)){
          error("pyFunction - dump(fileName) - a file name is needed");
        }
        cpp_Function->print(file_name);
      }
    }
    else{
      error("pyFunction. You should call dump() or dump(file_name)");
    }
    Py_INCREF(Py_None);
    return Py_None;
  }

 	/** It will return 1 if it is success and 0 otherwise */
  static PyObject* Function_normalize(PyObject *self, PyObject *args){
	  Function* cpp_Function = (Function*)((pyORBIT_Object*) self)->cpp_obj;
		return Py_BuildValue("i",cpp_Function->normalize());
  }

  //-----------------------------------------------------
  //destructor for python Function class (__del__ method).
  //-----------------------------------------------------
  static void Function_del(pyORBIT_Object* self){
		//std::cerr<<"The Function __del__ has been called!"<<std::endl;
		delete ((Function*)self->cpp_obj);
		self->ob_base.ob_type->tp_free((PyObject*)self);
  }

	// defenition of the methods of the python Function wrapper class
	// they will be vailable from python level
  static PyMethodDef FunctionClassMethods[] = {
		{ "add",				 	   Function_add,    	    METH_VARARGS,"Adds (x,y) to the Function container."},
		{ "getSize",		 	   Function_getSize,    	METH_VARARGS,"Returns the number of (x,y) in Function"},
		{ "getXYErrLists",   Function_getLists,   	METH_VARARGS,"Returns tuple (x_arr,y_arr,err_arr) "},
		{ "initFromLists",   Function_addLists,   	METH_VARARGS,"Initialize Function from lists of (x_arr,y_arr[,err_arr])."},
		{ "x",				       Function_x,          	METH_VARARGS,"Returns x value for a point with a particular index"},
 		{ "y",				       Function_y,    	      METH_VARARGS,"Returns y value for a point with a particular index"},
 		{ "err",			       Function_err,    	    METH_VARARGS,"Returns err value for y with a particular index"},
 		{ "xy",				       Function_xy,    	      METH_VARARGS,"Returns (x,y) value for a point with a particular index"},
 		{ "xyErr",				   Function_xyErr,    	  METH_VARARGS,"Returns (x,y,err) value for a point with a particular index"},
 		{ "removePoint",	   Function_removePoint,  METH_VARARGS,"Removes a point with a particular index from the Function"},
 		{ "updatePoint",	   Function_updatePoint,  METH_VARARGS,"Updates y or y,err values for a point with a particular index"},
 		{ "getMinX",		 	   Function_getMinX,    	METH_VARARGS,"Returns the minimal x value in the Function"},
 		{ "getMaxX",		 	   Function_getMaxX,    	METH_VARARGS,"Returns the maximal x value in the Function"},
 		{ "getMinY",		 	   Function_getMinY,    	METH_VARARGS,"Returns the minimal y value in the Function"},
 		{ "getMaxY",		 	   Function_getMaxY,    	METH_VARARGS,"Returns the maximal y value in the Function"},
 		{ "clean",			 	   Function_clean,    	  METH_VARARGS,"It will remove all points in the Function"},
 		{ "cleanMemory",	   Function_cleanMemory,  METH_VARARGS,"It will free the memory and remove all points in the Function"},
 		{ "getY",				 	   Function_getY,    	    METH_VARARGS,"Returns y for a specified x value "},
 		{ "getYP",				   Function_getYP,    	  METH_VARARGS,"Returns dy/dx for a specified x value "},
 		{ "getX",				 	   Function_getX,    	    METH_VARARGS,"Returns x for a specified y value "},
 		{ "getYErr",			   Function_getYErr,    	METH_VARARGS,"Returns err for a specified y value "},
 		{ "setConstStep",    Function_setConstStep, METH_VARARGS,"It will set the constant step flag to 1 if it is possible"},
 		{ "isStepConst", 	   Function_isStepConst,  METH_VARARGS,"It will return 1 if the step is const and 0 otherwise"},
 		{ "getStepEps", 	   Function_getStepEps,   METH_VARARGS,"It will return the constant step tolerance for x variable"},
 		{ "setStepEps", 	   Function_setStepEps,   METH_VARARGS,"It will set the constant step tolerance for x variable"},
 		{ "setInverse",		   Function_setInverse,   METH_VARARGS,"It will build the reverse Function if it is possible and return 1 or 0"},
 		{ "dump",				     Function_dump,    	    METH_VARARGS,"Prints Function into the std::cout stream or file"},
 		{ "normalize",	     Function_normalize,    METH_VARARGS,"It will return 1 if it is success and 0 otherwise"},
    {NULL}
  };

	// defenition of the memebers of the python Function wrapper class
	// they will be vailable from python level
	static PyMemberDef FunctionClassMembers [] = {
		{NULL}
	};

	//new python Function wrapper type definition
	static PyTypeObject pyORBIT_Function_Type = {
		PyVarObject_HEAD_INIT(NULL, 0)
		"Function", /*tp_name*/
		sizeof(pyORBIT_Object), /*tp_basicsize*/
		0, /*tp_itemsize*/
		(destructor) Function_del , /*tp_dealloc*/
		0, /*tp_print*/
		0, /*tp_getattr*/
		0, /*tp_setattr*/
		0, /*tp_compare*/
		0, /*tp_repr*/
		0, /*tp_as_number*/
		0, /*tp_as_sequence*/
		0, /*tp_as_mapping*/
		0, /*tp_hash */
		0, /*tp_call*/
		0, /*tp_str*/
		0, /*tp_getattro*/
		0, /*tp_setattro*/
		0, /*tp_as_buffer*/
		Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
		"The Function python wrapper", /* tp_doc */
		0, /* tp_traverse */
		0, /* tp_clear */
		0, /* tp_richcompare */
		0, /* tp_weaklistoffset */
		0, /* tp_iter */
		0, /* tp_iternext */
		FunctionClassMethods, /* tp_methods */
		FunctionClassMembers, /* tp_members */
		0, /* tp_getset */
		0, /* tp_base */
		0, /* tp_dict */
		0, /* tp_descr_get */
		0, /* tp_descr_set */
		0, /* tp_dictoffset */
		(initproc) Function_init, /* tp_init */
		0, /* tp_alloc */
		Function_new, /* tp_new */
	};



	//--------------------------------------------------
	//Initialization function of the pyFunction class
	//--------------------------------------------------
  void initFunction(PyObject* module){
		if (PyType_Ready(&pyORBIT_Function_Type) < 0) return;
		Py_INCREF(&pyORBIT_Function_Type);
		PyModule_AddObject(module, "Function", (PyObject *)&pyORBIT_Function_Type);

	}

#ifdef __cplusplus
}
#endif


}
