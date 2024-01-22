from art.db.update import UpdateArtSearchIdBatch

batch = UpdateArtSearchIdBatch()
batch.update("test-art-1", -1)
batch.update("test-art-2", -2)
batch.flush()
