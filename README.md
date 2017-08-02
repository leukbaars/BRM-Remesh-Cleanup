# BRM REMESH CLEANUP

This script is to be run after applying a remesh modifier on geometry.

It will:
- Clean up degenerate vertices
- Delete loose geometry
- Collapse very small faces
- Create a mesh that can be properly sculpted on
- Create a mesh that can be decimated nicely

WARNING!
Very dense meshes (+2 million tris) will potentially take a long time to clean (~60 seconds)
and could cause Blender to crash if it can't page enough RAM. Make sure you have plenty of
free memory and save before use. Ideally this script is best to be used on medium density remeshes (~500k>1million) which you can safely subdivide afterwards if you need more sculpting resolution

This is a really early test release, but already quite useful. It will likely change a lot in the future as I experiment with more cleanup methods.
