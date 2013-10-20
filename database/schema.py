import sqlalchemy as sa

DIRECTORY_STATUSES = ['new', 'failed', 'grouped', 'archived']
GROUPING_STATUSES = ['new', 'failed', 'combined']
FILE_STATUSES = ['new', 'failed', 'processed']
FILE_OBSTYPES = ['pulsar', 'cal']
FILE_STAGES = ['combined', 'corrected', 'cleaned', 'calibrated']

# Create metadata object
metadata = sa.MetaData()


# Define the metadata object
# Define versions table
sa.Table('versions', metadata, \
        sa.Column('version_id', sa.Integer, primary_key=True, \
                    autoincrement=True, nullable=False), \
        sa.Column('cg_githash', sa.String(64), nullable=False), \
        sa.Column('psrchive_githash', sa.String(64), nullable=False), \
        sa.UniqueConstraint('cg_githash', 'psrchive_githash'), \
        mysql_engine='InnoDB', mysql_charset='ascii')


# Define directoies table
sa.Table('directories', metadata, \
        sa.Column('dir_id', sa.Integer, primary_key=True, \
                    autoincrement=True, nullable=False), \
        sa.Column('path', sa.String(512), nullable=False, \
                    unique=True), \
#        sa.Column('status', sa.String(32), nullable=False, \
        sa.Column('status', sa.Enum(*DIRECTORY_STATUSES), nullable=False, \
                    default='new'), \
        sa.Column('added', sa.DateTime, nullable=False, \
                    default=sa.func.now()), \
        sa.Column('last_modified', sa.DateTime, nullable=False, \
                    default=sa.func.now()), \
        mysql_engine='InnoDB', mysql_charset='ascii')


# Define groupings table
sa.Table('groupings', metadata, \
        sa.Column('group_id', sa.Integer, primary_key=True, \
                    autoincrement=True, nullable=False), \
        sa.Column('dir_id', sa.Integer, \
                    sa.ForeignKey("directories.dir_id", name="fk_group_dir")), \
        sa.Column('version_id', sa.Integer, \
                    sa.ForeignKey("versions.version_id", name="fk_group_ver")), \
        sa.Column('listpath', sa.String(512), nullable=False), \
        sa.Column('listname', sa.String(512), nullable=False), \
        sa.Column('status', sa.Enum(*GROUPING_STATUSES), nullable=False, \
                    default='new'), \
        sa.Column('md5sum', sa.String(64), nullable=False, \
                    unique=True), \
        sa.Column('added', sa.DateTime, nullable=False, \
                    default=sa.func.now()), \
        sa.Column('last_modified', sa.DateTime, nullable=False, \
                    default=sa.func.now()), \
        mysql_engine='InnoDB', mysql_charset='ascii')


# Define groupings table
sa.Table('files', metadata, \
        sa.Column('file_id', sa.Integer, primary_key=True, \
                    autoincrement=True, nullable=False), \
        sa.Column('group_id', sa.Integer, \
                    sa.ForeignKey("groupings.group_id", name="fk_files_group")), \
        sa.Column('parent_file_id', sa.Integer, \
                    sa.ForeignKey("files.file_id", name="fk_files_file")), \
        sa.Column('version_id', sa.Integer, \
                    sa.ForeignKey("versions.version_id", name="fk_files_ver")), \
        sa.Column('filepath', sa.String(512), nullable=False), \
        sa.Column('filename', sa.String(512), nullable=False), \
        sa.Column('status', sa.Enum(*FILE_STATUSES), nullable=False, \
                    default='new'), \
        sa.Column('obstype', sa.Enum(*FILE_OBSTYPES), nullable=False), \
        sa.Column('stages', sa.Enum(*FILE_STAGES), nullable=False), \
        sa.Column('md5sum', sa.String(64), nullable=False, \
                    unique=True), \
        sa.Column('filesize', sa.Integer, nullable=False), \
        sa.Column('added', sa.DateTime, nullable=False, \
                    default=sa.func.now()), \
        sa.Column('last_modified', sa.DateTime, nullable=False, \
                    default=sa.func.now()), \
        mysql_engine='InnoDB', mysql_charset='ascii')
