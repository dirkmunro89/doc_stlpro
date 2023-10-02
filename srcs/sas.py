#
import os
import sys
import vtk
import math
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy
#
def sas():
#
    par_deg=45. # degrees as per prusaslicer definition
    par_ovr=np.cos(np.deg2rad(180-par_deg))
#
    fln_inp='/srcs/non.stl'
#
    if '.stl' in fln_inp: # if being called upon init
        reader = vtk.vtkSTLReader()
        reader.SetFileName(fln_inp)
        reader.Update()
        ply=reader.GetOutput()
    else:
        print('... stl expected')
        stop
#
    nrm_flt=vtk.vtkPolyDataNormals()
    nrm_flt.SetInputData(ply)
    nrm_flt.ComputeCellNormalsOn()
#   norm.SetAutoOrientNormals(True)
    nrm_flt.Update()
    ply=nrm_flt.GetOutput()
#
#   writer = vtk.vtkXMLPolyDataWriter()
#   writer.SetFileName('out.vtp')
#   writer.SetInputData(ply)
#   writer.Write()
#
    nrm=vtk_to_numpy(ply.GetCellData().GetArray('Normals'))
#
    src_pts=vtk.vtkPoints()
    src_elm=vtk.vtkCellArray()
    src_ply=vtk.vtkPolyData()
#
    snk_pts=vtk.vtkPoints()
    snk_elm=vtk.vtkCellArray()
    snk_ply=vtk.vtkPolyData()
#
    j1=0
    j2=0
    for i in range(ply.GetNumberOfCells()):
        if nrm[i,2] < par_ovr: # source
            ids=vtk.vtkIdList(); ply.GetCellPoints(i,ids)
            p1=np.array(ply.GetPoint(ids.GetId(0)))
            p2=np.array(ply.GetPoint(ids.GetId(1)))
            p3=np.array(ply.GetPoint(ids.GetId(2)))
            src_pts.InsertPoint(j1*3+0, p1[0], p1[1], p1[2])
            src_pts.InsertPoint(j1*3+1, p2[0], p2[1], p2[2])
            src_pts.InsertPoint(j1*3+2, p3[0], p3[1], p3[2])
            ids_i = vtk.vtkIdList()
            ids_i.InsertNextId(j1*3+0); ids_i.InsertNextId(j1*3+1); ids_i.InsertNextId(j1*3+2)
            src_elm.InsertNextCell(ids_i)
            j1=j1+1
        if nrm[i,2] < 0: # project shadow to serve as sink (support on part not yet allowed)
            ids=vtk.vtkIdList(); ply.GetCellPoints(i,ids)
            p1=np.array(ply.GetPoint(ids.GetId(0)))
            p2=np.array(ply.GetPoint(ids.GetId(1)))
            p3=np.array(ply.GetPoint(ids.GetId(2)))
            snk_pts.InsertPoint(j2*3+0, p1[0], p1[1], 0.)
            snk_pts.InsertPoint(j2*3+1, p2[0], p2[1], 0.)
            snk_pts.InsertPoint(j2*3+2, p3[0], p3[1], 0.)
            ids_i = vtk.vtkIdList()
            ids_i.InsertNextId(j2*3+0); ids_i.InsertNextId(j2*3+1); ids_i.InsertNextId(j2*3+2)
            snk_elm.InsertNextCell(ids_i)
            j2=j2+1
#
    src_ply.SetPoints(src_pts)
    src_ply.SetPolys(src_elm)
    snk_ply.SetPoints(snk_pts)
    snk_ply.SetPolys(snk_elm)
#
    writer = vtk.vtkSTLWriter()
    writer.SetFileName('/srcs/src.stl')
    writer.SetInputData(src_ply)
    writer.Write()
#
    writer = vtk.vtkSTLWriter()
    writer.SetFileName('/srcs/snk.stl')
    writer.SetInputData(snk_ply)
    writer.Write()
#
