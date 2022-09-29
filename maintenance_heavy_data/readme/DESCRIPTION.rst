Makes some adjustments to Maintenance app in some processes affected when
database has a heavy load:

* For kanban maintenance team view (dashboard), a more efficient
  ``search_count`` usage for counts, as v13 and later implement.
* For kanban equipments view, removes unncessary field, that makes faster
  view load.
