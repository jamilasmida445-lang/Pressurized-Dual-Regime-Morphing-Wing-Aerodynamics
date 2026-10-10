from paraview.simple import *
import os, json

foam_file = os.path.abspath("case.foam")
res = {"p_min": "N/A", "p_max": "N/A", "U_max": "N/A", "T_max": "N/A"}

if os.path.exists(foam_file):
    try:
        reader = OpenFOAMReader(registrationName='case.foam', FileName=foam_file)
        reader.MeshRegions = ['internalMesh']
        reader.UpdatePipelineInformation()
        
        for attr in ['CellArrays', 'PointArrays']:
            if hasattr(reader, attr):
                try: setattr(reader, attr, getattr(reader, attr).GetAvailable())
                except: pass

        timesteps = reader.TimestepValues
        if timesteps and len(timesteps) > 0:
            UpdatePipeline(time=timesteps[-1], proxy=reader)
        else:
            UpdatePipeline()

        data = servermanager.Fetch(reader)

        def extract_from_dataset(ds):
            if ds is None: return
            for cd in [ds.GetCellData(), ds.GetPointData()]:
                if cd is None: continue
                if res["p_min"] == "N/A" and cd.GetArray('p'):
                    r = cd.GetArray('p').GetRange()
                    res["p_min"] = round(r[0], 2)
                    res["p_max"] = round(r[1], 2)
                if res["U_max"] == "N/A" and cd.GetArray('U'):
                    u_arr = cd.GetArray('U')
                    u_max = max([(v[0]**2 + v[1]**2 + (v[2]**2 if len(v)>2 else 0))**0.5 for v in [u_arr.GetTuple(i) for i in range(u_arr.GetNumberOfTuples())]])
                    res["U_max"] = round(u_max, 2)
                if res["T_max"] == "N/A" and cd.GetArray('T'):
                    res["T_max"] = round(cd.GetArray('T').GetRange()[1], 2)

        if hasattr(data, 'NewIterator'):
            it = data.NewIterator()
            while not it.IsDoneWithTraversal():
                extract_from_dataset(it.GetCurrentDataObject())
                it.GoToNextItem()
        else:
            extract_from_dataset(data)

    except Exception as e:
        res["error"] = str(e)

with open("num_fields.json", "w") as f:
    json.dump(res, f)
