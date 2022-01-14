import kfp
from kfp import dsl
from kfp import onprem


@dsl.pipeline(
    name='Volume pipeline',
    description='A pipeline with volume.'
)
def volume_pipeline():
    vop = dsl.VolumeOp(
        name="pipeline-volume",
        resource_name="test01-pvc",
        modes=dsl.VOLUME_MODE_RWM,
        # RWO: Read, Write, Once; RWM: Read, Write, Many
        size="200Mi"
        # binary mega, mebibyte(MiB)
    )
    print(vop.volume)
    print(type(vop.volume))
    step1 = dsl.ContainerOp(
        name='caltech_download',
        image='stellapark401/caltech101:test',
        pvolumes={"/data": vop.volume}
    ).set_display_name('file_write').after(vop).apply(onprem.mount_pvc('test01-pvc', volume_name="pipeline-volume", volume_mount_path='/data'))


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(volume_pipeline,'pvc_specified.yaml')