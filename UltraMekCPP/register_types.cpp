#include "register_types.h"
//#include "ultramek.hpp"
#include "ultramek_gd.h"
#include <gdextension_interface.h>
#include <godot_cpp/core/class_db.hpp>
#include <godot_cpp/core/defs.hpp>
#include <godot_cpp/godot.hpp>

using namespace godot;

void initialize_ultramekgd_types(ModuleInitializationLevel p_level)
{
	if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) {
		return;
	}
	ClassDB::register_class<UltraMekGD>();
}

void uninitialize_ultramekgd_types(ModuleInitializationLevel p_level) {
	if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) {
		return;
	}
}

extern "C"
{

	// Initialization.
      GDExtensionBool GDE_EXPORT ultramekgd_library_init(
	    GDExtensionInterfaceGetProcAddress p_get_proc_address,
	    GDExtensionClassLibraryPtr p_library,
	    GDExtensionInitialization *r_initialization)
            {   
		GDExtensionBinding::InitObject init_obj(p_get_proc_address,p_library,
							r_initialization);
	

		init_obj.register_initializer(initialize_ultramekgd_types);
		init_obj.register_terminator(uninitialize_ultramekgd_types);
		init_obj.set_minimum_library_initialization_level(MODULE_INITIALIZATION_LEVEL_SCENE);

		return init_obj.init();
	}
}
